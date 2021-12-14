from django import urls
from django.urls import path
from . import views

urlpatterns = [
    # route: /app/
    path('', views.index),
    # route: /app/others/<x>
    path('others/<int:x>', views.dynamic),
]
