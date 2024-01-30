# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

# ! NON - PRIMARY OPERATION
# v1
# class CategoryListView(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# v2
# class CategoryListView(mixins.ListModelMixin,
#                        mixins.CreateModelMixin,
#                        generics.GenericAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         return self.create(request)

# v3


# class CategoryListView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# v1
# class ProductListView(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# v2
# class ProductListView(mixins.ListModelMixin,
#                       mixins.CreateModelMixin,
#                       generics.GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         return self.create(request)


# class ProductListView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


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

# v2
# class CategoryDetailView(mixins.RetrieveModelMixin,
#                          mixins.UpdateModelMixin,
#                          mixins.DestroyModelMixin,
#                          generics.GenericAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get(self, request, pk):
#         return self.retrieve(request, pk)

#     def put(self, request, pk):
#         return self.update(request, pk)

#     def delete(self, request, pk):
#         return self.destroy(request, pk)

# class ProductDetailView(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# v2

# class ProductDetailView(mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.DestroyModelMixin,
#                         generics.GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# class ProductReviewsView(APIView):

#     def get(self, request, product_id, review_id=None):
#         product = Product.objects.get(pk=product_id)

#         if review_id:
#             review = Review.objects.get(pk=review_id, product=product)
#             serializer = ReviewSerializer(review)
#             return Response(serializer.data)

#         reviews = Review.objects.filter(product=product)
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)

#     def post(self, request, product_id):
#         product = Product.objects.get(pk=product_id)
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(product=product)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, product_id, review_id):
#         product = Product.objects.get(pk=product_id)
#         review = Review.objects.get(pk=review_id, product=product)
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save(product=product)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, product_id, review_id):
#         product = Product.objects.get(pk=product_id)
#         review = Review.objects.get(pk=review_id, product=product)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# v2
# class ProductReviewsView(mixins.ListModelMixin,
#                          mixins.CreateModelMixin,
#                          mixins.RetrieveModelMixin,
#                          mixins.UpdateModelMixin,
#                          mixins.DestroyModelMixin,
#                          generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get_queryset(self):
#         product = get_object_or_404(Product, pk=self.kwargs['product_id'])
#         return Review.objects.filter(product=product)

#     def get_object(self):
#         if 'review_id' in self.kwargs:
#             return get_object_or_404(Review, pk=self.kwargs['review_id'])
#         else:
#             return None

#     def get(self, request, *args, **kwargs):
#         if 'review_id' in kwargs:
#             return self.retrieve(request, *args, **kwargs)
#         else:
#             return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         product = get_object_or_404(Product, pk=self.kwargs['product_id'])
#         return self.create(request, product=product, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         product = get_object_or_404(Product, pk=self.kwargs['product_id'])
#         return self.update(request, product=product, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         if 'review_id' in kwargs:
#             return self.destroy(request, *args, **kwargs)
#         else:
#             product = get_object_or_404(Product, pk=self.kwargs['product_id'])
#             Review.objects.filter(product=product).delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)


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
