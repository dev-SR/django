# Django Rest API

- [Django Rest API](#django-rest-api)
  - [Rest Framework Setup](#rest-framework-setup)
    - [Required Installations](#required-installations)
    - [env with `django-environ`](#env-with-django-environ)
    - [drf-spectacular](#drf-spectacular)
    - [`django-silk` for Profiling and Optimization](#django-silk-for-profiling-and-optimization)
    - [Exception Handling](#exception-handling)
  - [Introduction](#introduction)
    - [Serializers](#serializers)
    - [Basic RestApi CRUD Operations using DRF.](#basic-restapi-crud-operations-using-drf)
  - [Generic/Concrete View](#genericconcrete-view)
    - [For List and Create (non primary key based CRUD)](#for-list-and-create-non-primary-key-based-crud)
    - [For Retrieve, Update and Destroy (primary key based CRUD)](#for-retrieve-update-and-destroy-primary-key-based-crud)
    - [Overriding the default behavior](#overriding-the-default-behavior)
  - [Nested Serializer](#nested-serializer)
    - [Forward relation | the `One` side of `one-to-many` relation](#forward-relation--the-one-side-of-one-to-many-relation)
    - [Backward relation | the `Many` side of `one-to-many` relation](#backward-relation--the-many-side-of-one-to-many-relation)
    - [Complex nested serialization example](#complex-nested-serialization-example)
      - [ex1 : self-relation forward and backward relation](#ex1--self-relation-forward-and-backward-relation)
      - [ex2 Many to Many forward and backward](#ex2-many-to-many-forward-and-backward)
      - [Flattening nested serializer of backward relation | no no for POST/PUT](#flattening-nested-serializer-of-backward-relation--no-no-for-postput)
      - [Utilizing Model `@property` for backward relation serialization | no no for POST/PUT](#utilizing-model-property-for-backward-relation-serialization--no-no-for-postput)
    - [Tricky Post Request](#tricky-post-request)
      - [Create: Many to One / forward relation establishing](#create-many-to-one--forward-relation-establishing)
      - [Vanishing of `id` filed from request body schema | Adding forward relation by `id`](#vanishing-of-id-filed-from-request-body-schema--adding-forward-relation-by-id)
      - [Perform validation](#perform-validation)
      - [Create: Many to Many](#create-many-to-many)
      - [Update | many to one](#update--many-to-one)
  - [Customizing the ModelViewSet](#customizing-the-modelviewset)
  - [Pagination, search and filtering](#pagination-search-and-filtering)
    - [Pagination](#pagination)
      - [Global Pagination](#global-pagination)
      - [Custom pagination on an individual view](#custom-pagination-on-an-individual-view)
    - [Filtering](#filtering)
    - [Searching](#searching)
    - [Sorting](#sorting)
  - [ViewSets](#viewsets)
    - [ModelViewSets and Router](#modelviewsets-and-router)
  - [Authentication](#authentication)
    - [Protecting Routes with built-in permissions classes 🔥](#protecting-routes-with-built-in-permissions-classes-)
    - [JWT Authentication with simplejwt](#jwt-authentication-with-simplejwt)
      - [Setup](#setup)
      - [Basic Usage](#basic-usage)
  - [Complete Auth with djoser](#complete-auth-with-djoser)
    - [Custom User Model](#custom-user-model)
      - [Define model](#define-model)
      - [Admin and setting](#admin-and-setting)
    - [DJOSER configurations for jwt, email activation, social auth etc.](#djoser-configurations-for-jwt-email-activation-social-auth-etc)
    - [Customizing Serializers, cookies based token handling, errors](#customizing-serializers-cookies-based-token-handling-errors)
      - [Custom Serializers](#custom-serializers)
      - [Cookie based authentication and Authorization](#cookie-based-authentication-and-authorization)
      - [Custom Error Handling](#custom-error-handling)

## Rest Framework Setup

### Required Installations

1. Step1 : Installations

```bash
uv add django django-extensions djangorestframework django-filter django-environ
# start django project
uv run django-admin startproject config .
uv run manage.py migrate
uv run manage.py createsuperuser --username admin --email admin@example.com

#uv add Faker faker_commerce
```

2. Add `'rest_framework'`,`django-extensions` to your `INSTALLED_APPS` setting.
3. Test api 

`config/api_views.py`
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TestApiView(APIView):
    def get(self, request):
        return Response({"hello": "world"}, status=status.HTTP_200_OK)
```

`config/urls.py` 

```python
from django.contrib import admin
from django.urls import path
from .api_views import TestApiView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", TestApiView.as_view()),
]
```

### env with `django-environ`

```bash
uv add django-environ
```

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import environ
env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR / ".env", overwrite=True)
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", cast=bool, default=True)
```

### drf-spectacular 

```bash
uv add drf-spectacular
```

then add drf-spectacular to installed apps in settings.py

```python
INSTALLED_APPS = [
    # ALL YOUR APPS
    'drf_spectacular',
]
```

and finally register our spectacular AutoSchema with DRF.

```python
REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
SPECTACULAR_SETTINGS = {
    "TITLE": "DRF API",
    "DESCRIPTION": "project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # SCHEMA_PATH_PREFIX  is mainly used for tag extraction, where paths like '/api/v1/albums' with
    # a SCHEMA_PATH_PREFIX regex '/api/v[0-9]' would yield the tag 'albums'.
    "SCHEMA_PATH_PREFIX": "/api/",
}
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
```

Now, serve your schema from your API.

```python
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", TestApiView.as_view()),
    # drf_spectacular: [mandatory for swagger-ui, redoc to work]
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
```


- View ui : `http://127.0.0.1:8000/api/schema/swagger-ui/`


- Downloading schema file: Hitting url: `http://localhost:8000/api/schema/` will download the openapi `schema.yml` file

- Typescript type generation with[https://github.com/ferdikoomen/openapi-typescript-codegen](https://github.com/ferdikoomen/openapi-typescript-codegen): example command: `npx openapi-typescript-codegen --input http://localhost:8000/api/schema/ --output ./ts_type_generated  --useOptions --useUnionTypes --client axios`



### `django-silk` for Profiling and Optimization 

1. Installations: 

```bash
uv add django-silk
```

2. In `settings.py` add the following:

```python
MIDDLEWARE = [
    ...
    'silk.middleware.SilkyMiddleware',
    ...
]

INSTALLED_APPS = (
    ...
    'silk'
)
```

To enable access to the user interface add the following to your `config/urls.py`:

```python
if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
```

before running migrate:

```bash
python manage.py migrate
```

Silk will automatically begin interception of requests and you can proceed to add profiling if required. The UI can be reached at `/silk/`

### Exception Handling 

To send flatten error messages we can Overriding the Default DRF Exception Handler

`config\utils.py`

```python

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler to flatten all errors into a single string.
    """
    # Call the default DRF exception handler to get the default response
    response = exception_handler(exc, context)

    if response is not None:
        # Flatten the errors into a single string
        errors = []
        if isinstance(response.data, dict):
            for key, value in response.data.items():
                if isinstance(value, list):  # Handle lists of errors
                    errors.append(f"{key}: {', '.join(str(v) for v in value)}")
                else:  # Handle single error messages
                    errors.append(f"{key}: {value}")

        # Combine all error messages into a single string
        response.data = {"errors": ", ".join(errors)}

    return response

```

In `settings.py`, we have to point to the custom exception handler:

```python
REST_FRAMEWORK = {
    #<!-- -->
    "EXCEPTION_HANDLER": "config.utils.custom_exception_handler",
}
```


## Introduction

Django REST Framework (DRF) is a widely-used, full-featured API framework designed for building RESTful APIs with Django. At its core, DRF integrates with Django's core features -- **models, views, and URLs** -- making it simple and seamless to create a RESTful API.

The core concepts:

- Serializers
- Routers
- Views and ViewSets
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


`api_views.py`

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

## Generic/Concrete View


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

### Overriding the default behavior

These built-in classes can be overridden to provide custom behavior. Alt these classed are built on the top of `Mixins`

Detailed information can be found in the [https://www.cdrf.co/](https://www.cdrf.co/)

Example of overriding queryset:

```python
class UserOrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("order_items__product")
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user__username=self.request.user.username)
```

Example of overriding permission_classes:

```python
class ProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
```


## Nested Serializer

When working with nested data models, it’s common to need additional context or data from related models in API responses. By default, serializers in DRF mirror the model structure directly. However, we can enhance them to include forward (foreign key) or backward (related name) relations.


`models.py`

```python
class Category(models.Model):
    id = models.PrimaryKeyField()
    name = models.CharField()
    
class Product(models.Model):
    id = models.PrimaryKeyField()
    name = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
```

`serializers.py`

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

output: 

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

We can see Serializer output fields are similar to model fields. 

- `CategoryModel[id,name]` fields are mapped to `CategorySerializer[id,name]`. 
- `ProductModel[id,name,category]` fields are mapped to `ProductSerializer[id,name,category]`

> Note that `list of products` of a `Category` is completely missing and `category` of a `Product` is presented with `id` only

so: 
- How do we get list of `products` object backward relation `CategorySerializer[id,name,[products]`?
- How do we get `category` object in forward relation `ProductSerializer[id,name,[category]`?


### Forward relation | the `One` side of `one-to-many` relation

To define the `category` field in `ProductSerializer`, we use `CategorySerializer` to embed the full object instead of just the `id`. This allows nesting of related objects on the `one` side of a `one-to-many` relationship.

```python
class ProductSerializer(serializers.ModelSerializer):
    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ['id','name']
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
    "name": "HP envy x360",
    "price":1200
}
```


### Backward relation | the `Many` side of `one-to-many` relation

Using the `related_name` (`products`) in the `CategorySerializer`, we fetch all related Product objects. By setting `many=True`, DRF knows this is a list of items. The `ProductSerializer` ensures the nested objects are serialized correctly.

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "products",
        )

    class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("id", "name", "price",...)

    products = ProductSerializer(many=True, read_only=True)

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
            "price": 1100
        },
        {
            "id": 2,
            "name": "Dell XPS 13",
            "price": 1200
        }
        // ....
    ]
}
```


### Complex nested serialization example


#### ex1 : self-relation forward and backward relation

Desired Output:

```json
[
  {
    "id": "",
    "name": "",
    "parent": { }, //forward
    "subcategories": [],//backward
    "products": []//backward
  },
]
```
`models.py`

```python
class Category(models.Model):
    id = models.PrimaryKeyField()
    name = models.CharField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
    )

class Product(models.Model):
    id = models.PrimaryKeyField()
    name = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
```

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parent",
            "subcategories",
            "products",
            # "parent_v2", # using SerializerMethodField
            # "subcategories_v2", # using SerializerMethodField
        )

    class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("id", "name", "price", "stock", "status")

    products = ProductSerializer(many=True, read_only=True)

    class ParentCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ("id", "name")

    parent = ParentCategorySerializer(read_only=True)

    class SubcategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ("id", "name")

    subcategories = SubcategorySerializer(many=True, read_only=True)


    # subcategories_v2 = serializers.SerializerMethodField()

    # def get_subcategories_v2(self, obj):
    #     """Recursively serialize subcategories."""
    #     subcategories = obj.subcategories.all()
    #     return CategorySerializer(subcategories, many=True).data

    # parent_v2 = serializers.SerializerMethodField()

    # def get_parent_v2(self, obj):
    #     """Serialize the parent object."""
    #     parent = obj.parent
    #     if parent:
    #         return {"id": parent.id, "name": parent.name}
```

#### ex2 Many to Many forward and backward

Desired Output:

`models.py`  

```python
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    shipping_address = models.TextField()

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.item_subtotal for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
```

Expected output:
```json
[
  {
    "id": "",
    "user": {},
    "shipping_address": "",
    "status": "shipped",
    "total_price": 0,
    "created_at": "",
    "updated_at": "",
    "order_items": []
  }
]
```



`serializers.py`

```python
class OrderItemSerializer(serializers.ModelSerializer):
    class NestedOrderProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = [
                "id",
                "name",
                "price",
            ]

    product = NestedOrderProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
        ]
        read_only_fields = ["item_subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "username", "email"]

    user = UserSerializer()

    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",  # forward relation
            "shipping_address",
            "status",
            "order_items",  #backward relation
        ]
        read_only_fields = [ 
            "total_price",
            "created_at",
            "updated_at",
        ]
```


#### Flattening nested serializer of backward relation | no no for POST/PUT

```python
class OrderItemSerializer(serializers.ModelSerializer):
    class NestedOrderProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = [
                "id",
                "name",
                "price",
            ]

    product = NestedOrderProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
            "item_subtotal",
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = [
            "id",
            "shipping_address",
            "status",
            "total_price",
            "order_items",  #backward relation
        ]
```

This gives output in the following format:

```python
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "shipping_address": "string",
    "status": "pending",
    "total_price": 0,

    "order_items": [
      {
        "product": {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "name": "string",
          "price": 99999999
        },
        "quantity": 0,
        "item_subtotal": 0
      }
    ],
  }
]
```

So the `product` details is nested in as `product` object. We can flatten this object with serializer fields's `source` property:


```python
class OrderItemSerializer(serializers.ModelSerializer):
    # class NestedOrderProductSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Product
    #         fields = [
    #             "id",
    #             "name",
    #             "price",
    #         ]
    # product = NestedOrderProductSerializer(read_only=True)
    
    # FLATTENING NESTED PRODUCT FIELDS:
    product_id = serializers.UUIDField(source="product.id")
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )


    class Meta:
        model = OrderItem
        fields = [
            # "product",
            "product_id",
            "product_name",
            "product_price",
            "quantity",
            "item_subtotal",
        ]
```

Now we will get flattened output:


```python
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    # ....
    "order_items": [
      {
        "product_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "product_name": "string",
        "product_price": 99999999,
        "quantity": 0,
        "item_subtotal": 0
      }
    ],

  }
]
```

> Note that Although output is flatten, **for `POST` request, request body will be deserialize in non-flatten form** : ""product": {"id": "uuid","name": "string","price": 99999999},"


#### Utilizing Model `@property` for backward relation serialization | no no for POST/PUT

In [Flattening nested serializer of backward relation | no no for POST/PUT](#flattening-nested-serializer-of-backward-relation--no-no-for-postput), we saw for backward relation serialization it's cumbersome to define the nested serializer fields. instead we can utilize the model `@property` to serialize the nested relation. Lets define `ordered_products` property in `Order` model, which will replace `OrderItemSerializer` in `OrderSerializer`

```python
from typing import Optional, TypedDict, List
# for better swagger schema definition
class OrderedProductType(TypedDict):
    product_id: uuid.UUID
    product_name: str
    product_price: float
    product_quantity: int
    product_subtotal: float

class Order(models.Model):
    # ......
    @property
    def ordered_products(self) -> List[OrderedProductType]:
        """List all products in the order."""
        return [
            {
                "product_id": item.product.id,
                "product_name": item.product.name,
                "product_price": item.product.price,
                "product_quantity": item.quantity,
                "product_subtotal": item.item_subtotal,
            }
            for item in self.order_items.all()
        ]
        
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    # ....
```

So in `OrderSerializer` we can define the `ordered_products` field as follows:


```python
class OrderSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "username", "email"]

    user = UserSerializer()

    # order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",  # forward relation
            "shipping_address",
            "status",
            "total_price",
            "created_at",
            "updated_at",
            # "order_items",  #
            "ordered_products",
        ]
```

Output:

```python
[
  {
    # ...
    "ordered_products": [
      {
        "product_id": "string",
        "product_name": "string",
        "product_price": 0,
        "product_quantity": 0,
        "product_subtotal": 0
      }
    ]
  }
]
```

> PROS: Note that with this approach, the nested `product` is flattened
> CONS: Note that `POST` fields `ordered_products` will not be allowed

### Tricky Post Request

#### Create: Many to One / forward relation establishing

```python
class ProductSerializer(serializers.ModelSerializer):
    class CategorySerializer1(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ("id", "name")

    category = CategorySerializer1()

    class Meta:
        model = Product
        # fields = "__all__"
        fields = ["id", "name", "description", "price", "stock", "status", "category"]
```

In above serializer class `ProductSerializer`, the request body for the forward relation `category` is as follows:

```python
{
  "name": "string",
  "description": "string",
  "price": int,
  "stock": int,
  "status": "active",
  "category": {
    "name": "string"
  }
}
```

But upon a POST request with above request body, we will below error:

> AssertionError: The `.create()` method does not support writable nested fields by default. Write an explicit `.create()` method for serializer `orm.serializers.ProductSerializer`, or set `read_only=True` on nested serializer fields.

The `ProductSerializer` includes a nested serializer for the `category` field (`CategorySerializer1`). The incoming POST request tries to include a nested object for `category`, but DRF cannot automatically handle the creation or update of related objects for nested serializers.

The error suggests:

1. ✔️ Define a custom `create()` method to handle the nested category.
2. ❌ Alternatively, set `read_only=True` for the nested category serializer field (not desirable if you need to allow creating/updating nested objects).

If you also need to handle updates for nested serializers, implement the `update()` method as follows:

```python
class ProductSerializer(serializers.ModelSerializer):
    class CategorySerializer1(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ("id", "name")

    category = CategorySerializer1()

    class Meta:
        model = Product
        # fields = "__all__"
        fields = ["id", "name", "description", "price", "stock", "status", "category"]

    def create(self, validated_data):
        # Extract nested data for category
        category_data = validated_data.pop("category")
        # Fetch an existing Category matching the name or create a new one.
        category, created = Category.objects.get_or_create(**category_data)
        # Create the product with the associated category
        product = Product.objects.create(category=category, **validated_data)
        return product

```


#### Vanishing of `id` filed from request body schema | Adding forward relation by `id`

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    class CategorySerializer1(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ("id", "name")

    category = CategorySerializer1()
```

In above serializer class `ProductSerializer`, the request body for the forward relation `category` is as follows:

```python
{
  "name": "string",
  "description": "string",
  "price": int,
  "stock": int,
  "status": "active",
  "category": {
    "name": "string"
  }
}
```


> Notice Although we have `fields = ("id", "name")`, the `id` is not added on the request body for the forward relation `category`.?? 

That's mean we can not use `id` to get the `category` object. This is because The default implicitly-generated `id` field is marked as `read_only`. You will need to add an explicit `id` field to the instance serializer.

```python
class ProductSerializer(serializers.ModelSerializer):
    class CategorySerializer1(serializers.ModelSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField(read_only=True)

        class Meta:
            model = Category
            fields = ["id", "name"]

    category = CategorySerializer1()

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        category_data = validated_data.pop("category", None)
        category_id = category_data["id"]
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product
```

#### Perform validation


> Notice in `create()` method we are getting validated request body. Therefore it would be ideal to override the `validate()` method for all the validation logic.

```python
class ProductSerializer(serializers.ModelSerializer):
    class CategorySerializer1(serializers.ModelSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField(read_only=True)

        class Meta:
            model = Category
            fields = ["id", "name"]

    category = CategorySerializer1()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "status",
            "category",
        ]

    def validate(self, data):
        """Perform cross-field validation for all fields."""
        # Validate if a product with the same name exists
        if Product.objects.filter(name=data["name"]).exists():
            raise serializers.ValidationError(
                {"name": "A product with the same name already exists."}
            )

        # Ensure stock is valid when the status is active
        if data["status"] == Product.Status.ACTIVE and data["stock"] <= 0:
            raise serializers.ValidationError(
                {"status": "Active products must have a stock greater than zero."}
            )

        # Ensure price is within a reasonable range
        if data["price"] <= 0 or data["price"] > 99999999.00:
            raise serializers.ValidationError(
                {"price": "Price must be greater than 0 and less than 99,999,999.00."}
            )

        # Ensure the category is assigned and exists
        category_data = data.get("category")
        category_id = category_data.get("id")
        if not category_data:
            raise serializers.ValidationError(
                {"category": "Category must be provided and cannot be null."}
            )

        print(category_id)
        if not category_id:
            raise serializers.ValidationError(
                {"category": "Category ID must be provided."}
            )

        if not Category.objects.filter(id=category_id).exists():
            raise serializers.ValidationError(
                {"category": "The specified category does not exist."}
            )

        # Ensure product name length is reasonable
        if len(data["name"]) > 255:
            raise serializers.ValidationError(
                {"name": "Product name must not exceed 255 characters."}
            )

        # Ensure description length is within a limit
        if "description" in data and len(data["description"]) > 1000:
            raise serializers.ValidationError(
                {"description": "Description must not exceed 1000 characters."}
            )
        return data

    def create(self, validated_data):
        category_data = validated_data.pop("category", None)
        category_id = category_data["id"]
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product
```

This will make sure we are getting solid `validated_data` in `create()` and `update()` methods

Two important thing to note here:

1. If we have separate serializer for updating a product, there would be duplicate validation logic. One way to solve this problem is Using a Base Serializer Class. 

    ```python
    class BaseProductSerializer(serializers.ModelSerializer):
        def validate(self, data):
            return validate_product_data(data)

    class ProductListCreateSerializer(BaseProductSerializer):
        # CategorySerializer and other fields...
        def create(self, validated_data):
            # Create logic...
            pass
    class ProductRetrieveUpdateDestroySerializer(BaseProductSerializer):
        # CategorySerializer and other fields...
        def update(self, instance, validated_data):
            # Category handling and other update-specific logic...
            pass
    ```
This allows you to centralize validation logic in one place and reuse it across various serializers.

2. Throwing `raise serializers.ValidationError()` after each check will not capture remaining errors. To throw all the errors at once, below is the way:

```python
class BaseProductSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """Reusable validation method for product data."""
        errors = {}

        # Ensure stock is valid when the status is active
        if data["status"] == Product.Status.ACTIVE and data["stock"] <= 0:
            errors["status"] = "Active products must have a stock greater than zero."

        # Ensure price is within a reasonable range
        if data["price"] <= 0 or data["price"] > 99999999.00:
            errors["price"] = (
                "Price must be greater than 0 and less than 99,999,999.00."
            )

        # Ensure the category is assigned and exists
        category_data = data.get("category")
        if not category_data:
            errors["category"] = "Category must be provided and cannot be null."
        else:
            category_id = category_data.get("id")
            if not category_id:
                errors["category"] = "Category ID must be provided."
            elif not Category.objects.filter(id=category_id).exists():
                errors["category"] = "The specified category does not exist."

        # Ensure product name length is reasonable
        if len(data["name"]) > 255:
            errors["name"] = "Product name must not exceed 255 characters."

        # Ensure description length is within a limit
        if "description" in data and len(data["description"]) > 1000:
            errors["description"] = "Description must not exceed 1000 characters."

        # If there are any errors, raise them
        if errors:
            raise serializers.ValidationError(errors)

        return data
```

To send flatten error messages we can Overriding the Default DRF Exception Handler

`config\utils.py`

```python

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler to flatten all errors into a single string.
    """
    # Call the default DRF exception handler to get the default response
    response = exception_handler(exc, context)

    if response is not None:
        # Flatten the errors into a single string
        errors = []
        if isinstance(response.data, dict):
            for key, value in response.data.items():
                if isinstance(value, list):  # Handle lists of errors
                    errors.append(f"{key}: {', '.join(str(v) for v in value)}")
                else:  # Handle single error messages
                    errors.append(f"{key}: {value}")

        # Combine all error messages into a single string
        response.data = {"errors": ", ".join(errors)}

    return response

```

In `settings.py`, we have to point to the custom exception handler:

```python
REST_FRAMEWORK = {
    #<!-- -->
    "EXCEPTION_HANDLER": "config.utils.custom_exception_handler",
}
```


#### Create: Many to Many

Example Value:
Schema
```json
{
  "user": {
    "id": 1
  },
  "shipping_address": "string",
  "status": "pending",
  "order_items": [
    {
      "product": {
        "id": "b4ad1f21-69d0-4217-aecc-d3099f0b1c49"
      },
      "quantity": 0
    }
  ]
}
```


`models.py`

```python
class Product(models.Model):
    # ...
    def reduce_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError("Insufficient stock!")
        self.stock -= quantity
        self.save()

class Order(models.Model):
    # ...
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()

```

`serializer.py`

```python
class OrderItemListCreateSerializer(serializers.ModelSerializer):
    class NestedOrderProductSerializer(serializers.ModelSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField(read_only=True)
        price = serializers.DecimalField(
            max_digits=10, decimal_places=2, read_only=True
        )

        class Meta:
            model = Product
            fields = [
                "id",
                "name",
                "price",
            ]

    product = NestedOrderProductSerializer()
    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
            "item_subtotal",
        ]

class OrderListCreateSerializer(serializers.ModelSerializer):
    class OrderNestedUserSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField()
        username = serializers.CharField(read_only=True)  #
        email = serializers.EmailField(read_only=True)

        class Meta:
            model = User
            fields = ["id", "username", "email"]

    user = OrderNestedUserSerializer()
    order_items = OrderItemListCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",  # forward relation
            "shipping_address",
            "status",
            "total_price",
            "created_at",
            "updated_at",
            "order_items",  #
        ]

    def validate(self, data):
        """Perform cross-field validation for all fields."""

        # Extract user and order items
        user_data = data.get("user")
        order_items_data = data.get("order_items")

        # Validate user data
        if not user_data or not user_data.get("id"):
            raise serializers.ValidationError(
                {"user": "Valid User information is required."}
            )

        user = User.objects.filter(id=user_data["id"]).first()
        if not user:
            raise serializers.ValidationError(
                {"user": "User with the provided email does not exist."}
            )

        # Validate order items
        if not order_items_data:
            raise serializers.ValidationError(
                {"order_items": "At least one order item is required."}
            )

        # Check each order item
        for item_data in order_items_data:
            product_id = item_data["product"]["id"]
            product = Product.objects.filter(id=product_id).first()
            if not product:
                raise serializers.ValidationError(
                    {"order_items": f"Product with ID {product_id} does not exist."}
                )

            # check if quantity is zero
            quantity = item_data["quantity"]
            if quantity == 0:
                raise serializers.ValidationError(
                    {
                        "order_items": f"Quantity for product `{product.name}` cannot be zero."
                    }
                )

            # check if quantity is greater than stock
            if product.stock < quantity:
                raise serializers.ValidationError(
                    {"order_items": f"Insufficient stock for product `{product.name}`."}
                )

            # Check if the product is inactive
            if product.status == Product.Status.INACTIVE:
                raise serializers.ValidationError(
                    {"order_items": f"Product `{product.name}` is inactive."}
                )

        return data

    def create(self, validated_data):
        """Create order with validated data."""

        # Extract user and order items from validated data
        user_data = validated_data.pop("user")
        order_items_data = validated_data.pop("order_items")

        # Create the order
        user = User.objects.get(id=user_data["id"])
        order = Order.objects.create(user=user, **validated_data)

        # Create order items and reduce stock for each product
        for item_data in order_items_data:
            product = Product.objects.get(id=item_data["product"]["id"])
            quantity = item_data["quantity"]

            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            product.reduce_stock(quantity)  # Decrease stock after adding to order

        return order
```

#### Update | many to one 

`api_views.py`
```python
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductRetrieveUpdateDestroySerializer

    def get_permissions(self):
        # Restrict updates and deletes to admin users
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
```

```python
class ProductRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class CategoryRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
        id = serializers.UUIDField()
        name = serializers.CharField(read_only=True)

        class Meta:
            model = Category
            fields = [   # ...
            ]

    category = CategoryRetrieveUpdateDestroySerializer()

    class Meta:
        model = Product
        fields = [
            # ...
        ]
        read_only_fields = [
            # ...
        ]

    def update(self, instance, validated_data):
        # Extract category dict form request bod and add back category instance
        category_data = validated_data.pop("category", None)
        if category_data and isinstance(category_data, dict):
            category = Category.objects.get(id=category_data["id"])
            validated_data["category"] = category

        # Update the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate(self, data):
        """Perform cross-field validation for all fields."""
        return validate_product_data(data)
```


## Customizing the ModelViewSet

Example: Multiple route parameters
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

- [https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend](https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend)

The `django-filter` library includes a `DjangoFilterBackend` class which supports highly customizable field filtering for REST framework.

To use `DjangoFilterBackend`, first install django-filter.

```bash
uv add django-filter
```

Then add following in `settings.py`

```python
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]

REST_FRAMEWORK = {
    # ...
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

If all you need is simple equality-based filtering, you can set a `filterset_fields` attribute on the view, or viewset, listing the set of fields you wish to filter against.

`views.py`

```python
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer
    filterset_fields = ["name", "price"]
```

Example of advance `django_filters` usage: 
- [https://django-filter.readthedocs.io/en/stable/guide/usage.html](https://django-filter.readthedocs.io/en/stable/guide/usage.html)
- [https://django-filter.readthedocs.io/en/stable/ref/filterset.html](https://django-filter.readthedocs.io/en/stable/ref/filterset.html)


Define custom class for advance filtering:

`app\filters.py`

```python
from .models import Product
import django_filters
class ProductListFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ["name", "price"]
```

```python
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer
    # filterset_fields = ["name", "price"]
    filterset_class = ProductListFilter
```

This custom filter class can be now used for advice filtering:

```python
class ProductListFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
            "price": ["exact", "gte", "lte", "range"],
        }
```

Request ex:
- `http://127.0.0.1:8000/api/products/?price__range=10,10000`
- `'http://127.0.0.1:8000/api/products/?name__icontains=apple&price__gte=100&price__lte=1000'`


### Searching

- [https://www.django-rest-framework.org/api-guide/filtering/#searchfilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

The `SearchFilter` class from `rest_framework` supports simple single query parameter based searching, and is based on the Django admin's search functionality.


```python
from rest_framework import filters

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryCustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] # required
    filterset_fields = ['name']
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


## Authentication


### Protecting Routes with built-in permissions classes 🔥

**By default, DRF  authentication scheme uses Django's default session backend for authentication.** We can hence start protecting our endpoints with the permissions classes from `rest_framework.permissions`.


```python
from rest_framework.permissions import IsAuthenticated
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

- The IsAuthenticated permission applies to all HTTP methods (GET, POST, PUT, DELETE, etc.) on the endpoint.
- Only authenticated users can access any route managed by this viewset.
- No customization based on request type or user role.
- Best for: Scenarios where all actions under this viewset require the same level of protection.


```python
class ProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
            # self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductRetrieveUpdateDestroySerializer

    def get_permissions(self):
        # Restrict updates and deletes to admin users
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
```

- The permission changes based on the HTTP method.
  - For `GET` requests: The AllowAny permission allows all users, including unauthenticated ones, to access the endpoint.
  - For `POST/PUT/PATCH/DELETE` requests: The IsAdminUser permission restricts access to admin or authenticated users only.
- Best for: Scenarios where different actions on the endpoint require different levels of access control.


### JWT Authentication with simplejwt

- [#installation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation)
- [settings](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)

#### Setup


```bash
uv add djangorestframework-simplejwt
```

Project Configuration:


 In `settings.py`, add `rest_framework_simplejwt.authentication.JWTAuthentication` to the list of authentication classes:
 
 ```python
 REST_FRAMEWORK = {
    # ...
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",  # failure fallback + keep using django admin
    ],
}
```

Also, in your root `config/urls.py` file (or any other url config), include routes for Simple JWT’s `TokenObtainPairView` and `TokenRefreshView` views:

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]
```

#### Basic Usage

-  `api/token/` endpoint:  **Takes** a set of user credentials (by default `username` and `password`) and **returns** an `access` and `refresh` JSON web token pair to prove the authentication of those credentials.

    Usage:Get Token;

    ```python
    curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"username": "user", "password": "pass"}' \
    http://localhost:8000/api/token/

    ...
    {
    "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
    "refresh":"aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4....."
    }
    ```

    You can use the returned `access` token to prove authentication for a protected view:
    ```python
    curl \
    -H "Authorization: Bearer <access_token>" \
    http://localhost:8000/api/some-protected-view/
    ```

- `api/token/refresh/`: Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.When this short-lived access token expires, you can use the longer-lived refresh token to obtain another access token:

    ```python
    curl -X 'POST' \
    -H 'accept: application/json' \
    -d '{"refresh": "......"}'
    'http://127.0.0.1:8000/api/token/refresh/' \
    ---
    {
    "access": "....."
    }
    ```

## Complete Auth with djoser

```python
uv add django-cors-headers djoser
# or uv add django-cors-headers djoser djangorestframework_simplejwt social-auth-app-django
```

### Custom User Model

#### Define model

Before we begin let build a custom User model:
`account\models.py`

```python
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#a-full-example
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
import uuid


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email, password first_name and last_name
        """
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, password first_name and last_name
        """
        user = self.create_user(email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
```

#### Admin and setting


`account\admin.py`

```python
from django.contrib import admin
from .models import UserAccount
@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "created_at",
    )
    list_display_links = ("id", "email")
    list_filter = ("last_login", "is_active", "is_staff", "is_superuser")
    raw_id_fields = ("groups", "user_permissions")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("created_at",)

```

`config/setting.py`

```python
AUTH_USER_MODEL = "account.UserAccount"
```


> uv run manage.py createsuperuser --email e@gmail.com 


### DJOSER configurations for jwt, email activation, social auth etc.


``config/setting.py` 

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import environ
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
environ.Env.read_env(env_file=BASE_DIR / ".env", overwrite=True)

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG", cast=bool, default=True)
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", default="127.0.0.1,localhost".split(","))

# Application definition
INSTALLED_APPS = [
    # ...
    "djoser",
    "corsheaders",
    "social_django",  # Required for social auth
    # ...
    "account"
]
MIDDLEWARE = [
    # ...
    "corsheaders.middleware.CorsMiddleware",  # new
    "social_django.middleware.SocialAuthExceptionMiddleware",  # new social_django
    "django.middleware.common.CommonMiddleware",
    # ...
]
AUTH_USER_MODEL = "account.UserAccount"
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "config.utils.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "account.authentication.CustomJWTAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

DJOSER = {
    # https://djoser.readthedocs.io/en/latest/settings.html
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "ACTIVATION_URL": "/auth/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_CONFIRM_URL": "account/password_reset/{uid}/{token}",
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "SERIALIZERS": {
        "user": "account.serializers.UserSerializer",
        "current_user": "account.serializers.UserSerializer",
    },
    # social auth
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [
        "http://localhost:3000/auth/social/google",
        "http://localhost:3000/auth/social/github",
    ],
}

# social auth
# Social Auth settings
AUTHENTICATION_BACKENDS = [
    "social_core.backends.github.GithubOAuth2",  # Enable GitHub backend
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",  # Default auth backend
]

# GitHub App credentials (replace with your credentials)
SOCIAL_AUTH_GITHUB_KEY = env("GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = env("GITHUB_CLIENT_SECRET")

# JWT Setting
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=5),  # timedelta(days=1),minutes=5,seconds
    "UPDATE_LAST_LOGIN": True,
    "TOKEN_OBTAIN_SERIALIZER": "account.serializers.MyTokenObtainPairSerializer",
    # custom
    "AUTH_COOKIE": "access",  # cookie name
    "AUTH_COOKIE_DOMAIN": None,  # specifies domain for which the cookie will be sent
    "AUTH_COOKIE_SECURE": False,  # restricts the transmission of the cookie to only occur over secure (HTTPS) connections.
    "AUTH_COOKIE_HTTP_ONLY": True,  # prevents client-side js from accessing the cookie
    "AUTH_COOKIE_PATH": "/",  # URL path where cookie will be sent
    "AUTH_COOKIE_SAMESITE": "Lax",  # specifies whether the cookie should be sent in cross site requests
}

# Email Config
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SITE_NAME = "http://localhost:3000"  # used for creating email message: `You're receiving this email because you need to finish activation process on http://localhost:3000.
DOMAIN = "localhost:3000"  # used for creating activation URL: i.e. http://localhost:3000/activate/MTM/ch6ey6-7fbc56f343cd4e898a666f39bc3d9b38   # {{protocol}}://{{domain}}/{{url|safe}}
#Implementation at: .venv\Lib\site-packages\djoser\email.py
# CORS
CORS_ALLOWED_ORIGINS = env(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000".split(","),
)
CORS_ALLOW_CREDENTIALS = True
```

`config/urls.py`


```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # .....
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("account.urls")),
    # .....
]
```

### Customizing Serializers, cookies based token handling, errors

`account\urls.py`

```python
from django.urls import path, re_path
from .views import (
    CustomObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    CustomProviderAuthView,
    LogoutAPIView,
)

urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),
    path("jwt/create/", CustomObtainPairView.as_view()),
    path("jwt/refresh/", CustomTokenRefreshView.as_view()),
    path("jwt/verify/", CustomTokenVerifyView.as_view()),
    path("logout", LogoutAPIView.as_view()),
]
```

#### Custom Serializers

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        User = get_user_model()
        username_field = User.USERNAME_FIELD
        user = User.objects.filter(email=attrs[username_field]).first()
        # print(user)
        if not user:
            raise AuthenticationFailed(
                {"error": "Email or password is incorrect."},  # message}
                "no_active_account",  # code used by djoser
            )
        if not user.is_active:
            raise AuthenticationFailed(
                "Please activate your account first",
                "no_active_account",
            )
        data = super().validate(attrs)
        # sending user in response
        # user: UserAccount = self.user
        # data["user"] = {
        #     "id": str(user.id),
        #     "email": user.email,
        #     "role": "superuser"
        #     if user.is_superuser
        #     else "staff"
        #     if user.is_staff
        #     else "general",
        #     "is_activated": user.is_active,
        # }
        return data


class UserSerializer(DjoserUserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):  # <----vvi
        fields = ["id", "email", "first_name", "last_name", "role"]

    def get_role(self, obj):
        is_staff = obj.is_staff
        is_superuser = obj.is_superuser
        return "superuser" if is_superuser else "staff" if is_staff else "general"
```

#### Cookie based authentication and Authorization

`account\views.py`

```python
from django.conf import settings
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from djoser.social.views import ProviderAuthView


class CustomObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        print(f"my_{response.status_code}")

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            response.set_cookie(
                key="access",
                value=access_token,
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                max_age=int(
                    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
                ),
                domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.set_cookie(
                key="refresh",
                value=refresh_token,
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                max_age=int(
                    settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
                ),
                domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

        del response.data["access"]
        del response.data["refresh"]
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get("refresh")
        # print(request.COOKIES)
        if refresh_token:
            request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")
            response.set_cookie(
                key="access",
                value=access_token,
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                max_age=int(
                    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
                ),
                domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        access_token = request.COOKIES.get("access")
        # print(f"cookies:{request.COOKIES}")
        # print(f"access_token:{access_token}")
        # print(f"access_token:{type(access_token)}")
        if access_token:
            request.data["token"] = access_token
        return super().post(request, *args, **kwargs)


class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        # print(f"my_{args}")

        response = super().post(request, *args, **kwargs)
        print(f"my_{response.status_code}")
        if response.status_code == 201:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            response.set_cookie(
                key="access",
                value=access_token,
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                max_age=int(
                    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
                ),
                domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.set_cookie(
                key="refresh",
                value=refresh_token,
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                max_age=int(
                    settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
                ),
                domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
        # del response.data["access"]
        # del response.data["refresh"]
        return response
```

`account\authentication.py`

```python
from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

# def enforce_csrf(request):
#     """
#     Enforce CSRF validation.
#     """
#     check = CSRFCheck()
#     check.process_request(request)
#     reason = check.process_view(request, None, (), {})
#     if reason:
#         raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request):
        try:
            header = self.get_header(request)
            # print(header, request.COOKIES.get("access"))

            if header is None:
                raw_token = request.COOKIES.get("access") or None
            else:
                raw_token = self.get_raw_token(header)  ## Authorization: JWT <token>
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            # enforce_csrf(request)
            return self.get_user(validated_token), validated_token
        except Exception:
            return None
```


#### Custom Error Handling

`config\utils.py`

```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler to format all errors into a consistent structure.
    """
    # Call the default DRF exception handler to get the standard error response
    response = exception_handler(exc, context)
    print(response.data)

    if response is not None:
        # Check if `response.data` is a dictionary
        if isinstance(response.data, dict):
            # Format the dictionary into a consistent error structure
            formatted_errors = []
            for key, value in response.data.items():
                if isinstance(value, list):  # Field-specific errors
                    for error in value:
                        if key in ["non_field_errors"]:
                            key = None
                        formatted_errors.append({"field": key, "message": error})
                else:  # General error message
                    if key in ["detail"]:
                        key = None
                    formatted_errors.append({"field": key, "message": value})
        elif isinstance(response.data, list):  # Non-field-specific errors in a list
            formatted_errors = [
                {"field": None, "message": error} for error in response.data
            ]
        else:  # Handle other unexpected response data
            formatted_errors = [{"field": None, "message": str(response.data)}]

        # Create a unified response format
        response.data = {
            "success": False,
            "status_code": response.status_code,
            "errors": formatted_errors,
        }

    else:
        # Handle errors that DRF couldn't handle (e.g., JSON parsing errors)
        formatted_errors = [{"field": None, "message": str(exc)}]
        response = Response(
            {
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "errors": formatted_errors,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
```
