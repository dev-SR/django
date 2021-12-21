from django import urls
from django.urls import path
from . import views

urlpatterns = [
    # route: /app/
    path('', views.index, name='index'),
    # route: /app/others/<x>
    path('others/<str:x>', views.dynamic, name='others'),
]
