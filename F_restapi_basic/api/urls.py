from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# from .views import (CategoryDetailView, CategoryListView, ProductDetailView,
#                     ProductListView, ProductReviewsView)

from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories',  views.CategoryViewSet)
# router.register(r'products/(?P<product_id>\d+)/reviews', views.ProductReviewsViewSet, basename='product-reviews')
router.register(r'products/(?P<product_id>.*)/reviews', views.ProductReviewsViewSet, basename='product-reviews')


urlpatterns = [
    path("", include(router.urls)),
    # path('categories/', views.CategoryListView.as_view(), name='category-list'),
    # path('products/', views.ProductListView.as_view(), name='product-list'),
    # path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    # path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # path('products/<int:product_id>/reviews/', views.ProductReviewsView.as_view(), name='product-reviews'),
    # path('products/<int:product_id>/reviews/<int:review_id>/', views.ProductReviewsView.as_view(), name='review-detail'),
]
