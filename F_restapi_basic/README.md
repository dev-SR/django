# Django Rest API

- [Django Rest API](#django-rest-api)
  - [Installation](#installation)
  - [Introduction](#introduction)
    - [Serializers](#serializers)
    - [Basic RestApi CRUD Operations using DRF.](#basic-restapi-crud-operations-using-drf)
  - [Mixin in DRF](#mixin-in-drf)
    - [Mixin for List and Create (non primary key based CRUD)](#mixin-for-list-and-create-non-primary-key-based-crud)
    - [Mixin for Retrieve, Update and Destroy (primary key based CRUD)](#mixin-for-retrieve-update-and-destroy-primary-key-based-crud)
  - [Concrete View](#concrete-view)
    - [For List and Create (non primary key based CRUD)](#for-list-and-create-non-primary-key-based-crud)
    - [For Retrieve, Update and Destroy (primary key based CRUD)](#for-retrieve-update-and-destroy-primary-key-based-crud)
  - [ViewSets](#viewsets)
    - [ModelViewSets and Router](#modelviewsets-and-router)
  - [Pagination, search and filtering](#pagination-search-and-filtering)
    - [Pagination](#pagination)
      - [Global Pagination](#global-pagination)
      - [Custom pagination on an individual view](#custom-pagination-on-an-individual-view)
    - [Filtering](#filtering)
    - [Searching](#searching)
    - [Sorting](#sorting)
  - [More on  Serializer](#more-on--serializer)
    - [Changing output of the serializer](#changing-output-of-the-serializer)
    - [Nested Serializer](#nested-serializer)
  - [Customizing the ModelViewSet](#customizing-the-modelviewset)
  - [Multiple route parameters](#multiple-route-parameters)
  - [Token Authentication](#token-authentication)
    - [Configure Token Authentication](#configure-token-authentication)
    - [Automatically generate token for new user using signals](#automatically-generate-token-for-new-user-using-signals)
    - [Registers and login serializers](#registers-and-login-serializers)
    - [Registers and login view](#registers-and-login-view)
    - [Protecting Routes 🔥](#protecting-routes-)
  - [Related Fields in Django REST Framework](#related-fields-in-django-rest-framework)

## Installation

```bash
pipenv install djangorestframework
```

## Introduction

Django REST Framework (DRF) is a widely-used, full-featured API framework designed for building RESTful APIs with Django. At its core, DRF integrates with Django's core features -- **models, views, and URLs** -- making it simple and seamless to create a RESTful API.

The core concepts:

- Serializers
- Views and ViewSets
- Routers
- Authentication and Authorization

DRF is composed of the following components:

- `Serializers` are used to convert Django QuerySets and model instances to (serialization) and from (deserialization) JSON (and a number of other data rendering formats like XML and YAML). Otherwise, we will get  `TypeError: Object of type 'User' is not JSON serializable`
- `Views` (along with `ViewSets`), which are similar to traditional Django views, handle RESTful HTTP requests and responses. The view itself uses serializers to validate incoming payloads and contains the necessary logic to return the response. Viewsets are coupled with routers, which map the views back to the exposed URLs.

<p align="center">
<img src="img/ViewsSerializers.jpg" alt="ViewsSerializers.jpg" width="700px"/>
</p>

Although, DRF provides a number of ways to build APIs, the most common approach is to use a combination of `ModelSerializer` for serialization and `APIView` for views.

### Serializers

Again, serializers are used to convert Django QuerySets and model instances to and from JSON. Also, before deserializing the data, for incoming payloads, serializers validate the shape of the data.

Why does the data need to be (de)serialized?

Django QuerySets and model instances are Django-specific and, as such, not universal. In other words, the data structure needs to be converted into a simplified structure before it can be communicated over a RESTful API.

<p align="center">
<img src="img/serializer.jpg" alt="serializer.jpg" width="600px"/>
</p>

Readings:

- [https://testdriven.io/blog/drf-serializers](https://testdriven.io/blog/drf-serializers)

### Basic RestApi CRUD Operations using DRF.

`models.py`

```python
from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=255)
```

`serializers.py`

```python
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
```


`views.py`

1. Non-Primary Key Based CRUD Operations involving getting lists, creating new objects.

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Category
from .serializers import CategorySerializer


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```

2. Primary Key Based CRUD Operations involving getting a single object, updating an object, and deleting an object.


```python
from django.shortcuts import get_object_or_404
# ...
class CategoryDetail(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

```

`app/urls.py`

```python
from django.urls import path
from .views import CategoryList, CategoryDetail

urlpatterns = [
    # registering non-primary key based CRUD operations
    path('categories/', CategoryList.as_view(), name='category-list'),
    # registering primary key based CRUD operations
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail')
]
```

`config/urls.py`

```python
from django.urls import path, include

urlpatterns = [
    path('api/', include('app.urls')),
]
```


## Mixin in DRF

DRF provides a number of built-in generic class-based views that can be used to abstract common actions. These views are called `Mixins`.

The `GenericAPIView` also give HTML forms for the API endpoints.


### Mixin for List and Create (non primary key based CRUD)

```python
# v1
# class CategoryList(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# v2
from rest_framework import mixins, generics
class CategoryListView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
```

### Mixin for Retrieve, Update and Destroy (primary key based CRUD)

```python
# class CategoryDetailView(APIView):
#     def get(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         serializer = CategorySerializer(category, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         serializer = CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         category = get_object_or_404(Category, pk=pk)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryDetailView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
```




## Concrete View

The If you're using generic views this is normally the level you'll be working at unless you need heavily customized behavior.
The view classes can be imported from `rest_framework.generics`.

- ListAPIView
- CreateAPIView
- RetrieveAPIView
- UpdateAPIView
- DestroyAPIView
- ListCreateAPIView
- RetrieveUpdateAPIView
- RetrieveDestroyAPIView
- RetrieveUpdateDestroyAPIView


### For List and Create (non primary key based CRUD)

```python
from rest_framework import generics
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

### For Retrieve, Update and Destroy (primary key based CRUD)

```python
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

## ViewSets

### ModelViewSets and Router

ModelViewSet provides default create, retrieve, update, partial_update, destroy and list actions since it uses `GenericViewSet` and all of the available mixins.


- [https://testdriven.io/blog/drf-views-part-3/#modelviewset](https://testdriven.io/blog/drf-views-part-3/#modelviewset)


```python
from .serializers import CategorySerializer
from .models import Category

# class CategoryListView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

from rest_framework import viewsets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

ViewSets come with a router class that automatically generates the URL configurations.

DRF comes with two routers out-of-the-box:

- DefaultRouter
- SimpleRouter

The main difference between them is that `DefaultRouter` includes a default API root view:

Defining the router:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

# urlpatterns = [
#     path('categories/', CategoryList.as_view(), name='category-list'),
#     path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail')
# ]

router = DefaultRouter()
router.register("categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

```

Now at root level `http://127.0.0.1:8000/api/`, we can api root view.

```json
{
    "categories": "http://127.0.0.1:8000/api/categories/"
}
```

## Pagination, search and filtering

### Pagination

- [https://www.django-rest-framework.org/api-guide/pagination/](https://www.django-rest-framework.org/api-guide/pagination/)

#### Global Pagination

The pagination style may be set globally, using the `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` setting keys. For example, to use the built-in limit/offset pagination, you would do something like this:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5
}
```

#### Custom pagination on an individual view

If you want to modify particular aspects of the pagination style, you'll want to override one of the pagination classes, and set the attributes that you want to change.

```python
from rest_framework.pagination import PageNumberPagination
class CategoryCustomPagination(PageNumberPagination):
    page_size = 3

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryCustomPagination
```

### Filtering

- [https://www.django-rest-framework.org/api-guide/filtering/](https://www.django-rest-framework.org/api-guide/filtering/)

The `django-filter` library includes a `DjangoFilterBackend` class which supports highly customizable field filtering for REST framework.

To use `DjangoFilterBackend`, first install django-filter.

```bash
pipenv install django-filter
```

Then add 'django_filters' to Django's INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]
```

You should now either add the filter backend to your settings:

```python
REST_FRAMEWORK = {
    # ...
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

Or add the filter backend to an individual View or ViewSet.


```python
from django_filters.rest_framework import DjangoFilterBackend

class CategoryViewSet(viewsets.ModelViewSet):
    ...
    filter_backends = [DjangoFilterBackend]
```

If all you need is simple equality-based filtering, you can set a `filterset_fields` attribute on the view, or viewset, listing the set of fields you wish to filter against.

`views.py`

```python
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryCustomPagination
    filterset_fields = ['name']
```

### Searching

- [https://www.django-rest-framework.org/api-guide/filtering/#searchfilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

The `SearchFilter` class from `rest_framework` supports simple single query parameter based searching, and is based on the Django admin's search functionality.


```python
from rest_framework import filters

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryCustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    # filter_backends = [filters.SearchFilter]
    search_fields = ['name']
```

The search behavior may be specified by prefixing field names in `search_fields` with one of the following characters (which is equivalent to adding `__<lookup>` to the field):

- `^` Starts-with search.
- `=` Exact matches.
- `@` Full-text search.
- `$` Regex search.

```python
search_fields = ['=username', '=email']
```

### Sorting

- [https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

```python
class CategoryViewSet(viewsets.ModelViewSet):
    # ....
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
```

If an `ordering` attribute is set on the view, this will be used as the default ordering.

```python
class CategoryViewSet(viewsets.ModelViewSet):
    # ....
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['-id']
```




## More on  Serializer

### Changing output of the serializer

Two of the most useful functions inside the BaseSerializer class that we can override are to_representation() and `to_internal_value()`. By overriding them, we can change the serialization and deserialization behavior, respectively, to append additional data, extract data, and handle relationships.

- `to_representation()` allows us to change the serialization output - convert response to JSON.
- `to_internal_value()` allows us to change the deserialization output

More - [https://testdriven.io/blog/drf-serializers/#custom-outputs](https://testdriven.io/blog/drf-serializers/#custom-outputs)

Example of changing the output of the serializer:

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tags_count'] = instance.tags.count()
        return response
```

output:

```json
 {
    "id": 4,
    "name": "iPhone 15",
    "tags_count": 2
},
```

Example of changing the input of the serializer:

Suppose instead of making `POST` request below data format:

```python
{
  "name": "X",
  "category":2,
  "tags":[1,2]
}

we make the request like this:

```json
{
  "data":{
    "name": "X",
    "category":2,
    "tags":[1,2]
  }
}
```

So in `to_internal_value` method we need to extract the `data` key from the request data.

```python
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_internal_value(self, data):
        main_data = data['data']
        return super().to_internal_value(main_data)
```

### Nested Serializer

`models.py`

```python
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products')

    def __str__(self):
        return self.name

```


`serializers.py`

```python
from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```


Here 1 Category can have many products. But default the response will be like this:

```json
GET api/categories/
{
    "id": 1,
    "name": "Laptops"
}

GET api/products/
{
    "id": 1,
    "name": "HP envy x360",
    "category": 1
}
```

So, the relations fields are represented as primary keys for `many-to-one` side and not even represented for `one-to-many` or `many-to-many` side.

1. Populating `one-to-many` is simple, just use the `related_name` value, `products` in the case and define as a property with corresponding serializer class.

```python
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'
```

Here is the new response:

```json
GET api/categories/
{
    "id": 1,
    "name": "Laptops",
    "products": [
        {
            "id": 1,
            "name": "HP envy x360",
            "category": 1
        },
        {
            "id": 2,
            "name": "Dell XPS 13",
            "category": 1
        }
        // ....
    ]
}
```

2. Populating `many-to-one`:

As we've seen the category foreign filed in the product model is represented as a primary key.  To ge the whole category object, we need to define a property with the corresponding serializer class.

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'
```

```json
{
    "id": 1,
    "category": {
        "id": 1,
        "name": "Laptops"
    },
    "name": "HP envy x360"
}
```

**But this will brake the `POST` request**.

One option is to override `to_representation` method in the `ProductSerializer` class, in the many side.
We can override the `to_representation` function of the serializer to change the output of the serializer,



```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        return response
```

- [https://stackoverflow.com/questions/29950956/drf-simple-foreign-key-assignment-with-nested-serializers](https://stackoverflow.com/questions/29950956/drf-simple-foreign-key-assignment-with-nested-serializers)


3. Populating `many-to-many` side, with out breaking `POST` method is also to override the `to_representation` method.


`models.py`

```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products', blank=True, null=True)

    def __str__(self):
        return self.name
```

`serializers.py`

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        response['tags'] = TagSerializer(instance.tags, many=True).data

        return response
```

Example of making `POST` request with json data.

```json
POST api/products/
{
    "name": "HP envy x360",
    "category": 1,
    "tags": [1, 2]
}
```

4. `depth` option:

```python
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['category'] = CategorySerializer(instance.category).data
    #     response['tags'] = TagSerializer(instance.tags, many=True).data
    #     return response
```

But `POST` request will break.


4. Still, choosing nested serializer is a trade of between `one-to-many` and `many-to-one` relationships. Both can't be achieved at the same time because of circular dependency of the serializer classes.

There's also built-in Serializer relations like `PrimaryKeyRelatedField`, `HyperlinkedRelatedField`, `SlugRelatedField`, `HyperlinkedIdentityField`.

- [doc#relations](https://www.django-rest-framework.org/api-guide/relations/)

Note that **reverse relationships** are not automatically included by the `ModelSerializer` and `HyperlinkedModelSerializer` classes. To include a reverse relationship, you must explicitly add it to the fields list. For example:


```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'products']
        # fields = '__all__' will not include the reverse relationship, the `related_name` should be used.


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'products']
        # fields = '__all__' will not include the reverse relationship, the `related_name` should be used.


class ProductSerializer(serializers.ModelSerializer):
    # category = CategoryField(queryset=Category.objects.all())
    # tags = TagField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        response['tags'] = TagSerializer(instance.tags, many=True).data

        return response
```

You'll normally want to ensure that you've set an appropriate `related_name` argument,`products`,  on the relationship, that you can use as the field name explicitly instead of `__all__`.



- [doc#reverse-relations](https://www.django-rest-framework.org/api-guide/relations/#reverse-relations)




## Customizing the ModelViewSet

```python
class ProductReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if self.kwargs.get('review_id'):
            return Review.objects.filter(pk=self.kwargs['review_id'], product__pk=product_id)
        return Review.objects.filter(product__pk=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)
        serializer.save(product=product)

    def perform_update(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)
        serializer.save(product=product)

    def perform_destroy(self, instance):
        instance.delete()
```

```python
# ...
router.register(r'products/(?P<product_id>.*)/reviews', views.ProductReviewsViewSet, basename='product-reviews')
urlpatterns = [
    path("", include(router.urls)),
    # path('products/<int:product_id>/reviews/', views.ProductReviewsView.as_view(), name='product-reviews'),
    # path('products/<int:product_id>/reviews/<int:review_id>/', views.ProductReviewsView.as_view(), name='review-detail'),
]
```

## Multiple route parameters

```python
urlpatterns = [
    path('products/<int:product_id>/reviews/', ProductReviewsView.as_view(), name='product-reviews'),
    path('products/<int:product_id>/reviews/<int:review_id>/', ProductReviewsView.as_view(), name='review-detail'),
]
```

```python


class ProductReviewsView(APIView):

    def get(self, request, product_id, review_id=None):
        product = Product.objects.get(pk=product_id)

        if review_id:
            review = Review.objects.get(pk=review_id, product=product)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)

        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id, review_id):
        product = Product.objects.get(pk=product_id)
        review = Review.objects.get(pk=review_id, product=product)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, review_id):
        product = Product.objects.get(pk=product_id)
        review = Review.objects.get(pk=review_id, product=product)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

mixin

For complex route pattern, we have to customize the `queryset`.

```python
# v2
class ProductReviewsView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return Review.objects.filter(product=product)

    def get_object(self):
        if 'review_id' in self.kwargs:
            return get_object_or_404(Review, pk=self.kwargs['review_id'])
        else:
            return None

    def get(self, request, *args, **kwargs):
        if 'review_id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return self.create(request, product=product, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return self.update(request, product=product, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if 'review_id' in kwargs:
            return self.destroy(request, *args, **kwargs)
        else:
            product = get_object_or_404(Product, pk=self.kwargs['product_id'])
            Review.objects.filter(product=product).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
```


## Token Authentication

- [https://www.pythonworld.io/blogs/how-to-implement-token-authentication-in-django-and-django-rest-framework](https://www.pythonworld.io/blogs/how-to-implement-token-authentication-in-django-and-django-rest-framework)

### Configure Token Authentication

```python
# settings.py
INSTALLED_APPS = [
   ...
   'rest_framework.authtoken'
   ...
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

```

Run: `python manage.py migrate`

### Automatically generate token for new user using signals

`users\api\signals.py`

```python
# By generating token using signals is the best way. So here we actually use post_save signals, that will create a token, when new user will create.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

If you plan to use signals (ex: `signals.py`) within an app (ex: posts), simply get in the habit of adding this method to your apps.py `AppConfig` class everytime.

`users\apps.py`

```python
from django.apps import AppConfig
class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        from .api import signals
        return super().ready()
```

### Registers and login serializers

`users\api\serializers.py`

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    """override create method to change the password into hash."""

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(RegisterSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']
```

### Registers and login view

`users\api\views.py`

```python
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer


class RegisterAPIView(generics.GenericAPIView):
    """Handles user registration."""

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            """If the validation success, it will created a new user."""
            serializer.save()
            res = {'status': status.HTTP_201_CREATED}
            return Response(res, status=status.HTTP_201_CREATED)
        res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    """Handles user login and returns authentication token."""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                """We are reterving the token for authenticated user."""
                token = Token.objects.get(user=user)
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "data": {
                        "Token": token.key
                    }
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Email or Password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
```


### Protecting Routes 🔥

```python
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

## Related Fields in Django REST Framework

DRF tip:

To represent model relationships in a serializer, you can use various related fields that represent the target of the relationship in different ways:

- `StringRelatedField`
- `PrimaryKeyRelatedField`
- `HyperlinkedRelatedField`
- `SlugRelatedField`
- `HyperlinkedIdentityField`

Examples:

```python
class TagSerializer(serializers.ModelSerializer):

    posts = serializers.StringRelatedField(many=True)
    # result: ["My story" (from __str__ method)]


    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # result: [1]


    posts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='post-detail'
    )
    # result: ["http://127.0.0.1:8000/1/"]


    posts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
     )
    # result: ["My story" (from title field)]


    tag_detail = serializers.HyperlinkedIdentityField(view_name='tag-detail')
    # result: "http://127.0.0.1:8000/tags/1/"
    # *HyperlinkedIdentityField is used for current object, not related objects
```
