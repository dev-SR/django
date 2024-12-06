from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from orm.filters import ProductListFilter
from .models import Order, Product, Category
from .serializers import (
    OrderListCreateSerializer,
    ProductSerializer,
    ProductRetrieveUpdateDestroySerializer,
    OrderRetrieveUpdateDestroySerializer,
    CategorySerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class CategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ["name"]


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer
    # filterset_fields = ["name", "price"]
    filterset_class = ProductListFilter

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class UserOrderListApiView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related("order_items__product")
    serializer_class = OrderListCreateSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class UserOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.prefetch_related("order_items__product")
    serializer_class = OrderRetrieveUpdateDestroySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure that users can only access their own orders
        return self.queryset.filter(user=self.request.user)


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductRetrieveUpdateDestroySerializer

    def get_permissions(self):
        # Restrict updates and deletes to admin users
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
