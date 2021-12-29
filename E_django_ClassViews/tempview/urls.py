from django.urls import path
from . import views
urlpatterns = [
    path('', views.TempView.as_view(), name='tempview'),
    path('<int:id>/', views.TempDetailView.as_view(), name='tempdetail'),
]
