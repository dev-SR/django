# from .views import CategoryList, CategoryDetail
# urlpatterns = [
#     path('categories/', CategoryList.as_view(), name='category-list'),
#     path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail')
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, TagViewSet
router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("tags", TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
