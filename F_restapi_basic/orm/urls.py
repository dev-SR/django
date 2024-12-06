from django.urls import path
from orm.api_views import (
    ProductListCreateAPIView,
    CategoryAPIView,
    UserOrderListApiView,
    ProductRetrieveUpdateDestroyAPIView,
    UserOrderRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("categories/", CategoryAPIView.as_view()),
    path("products/", ProductListCreateAPIView.as_view()),
    path("products/<uuid:pk>/", ProductRetrieveUpdateDestroyAPIView.as_view()),
    path("orders/", UserOrderListApiView.as_view()),
    path("orders/<uuid:pk>/", UserOrderRetrieveUpdateDestroyAPIView.as_view()),
]
