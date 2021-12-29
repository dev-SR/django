from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListViewClass.as_view(), name='listview'),
    # Generic detail view DetailViewClass must be called with either an object pk or a slug in the URLconf.
    path('<int:pk>/', views.DetailViewClass.as_view(), name='detail'),
]
