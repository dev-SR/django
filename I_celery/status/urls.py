from django.urls import path
from . import views

urlpatterns = [
    path('task', views.check_status, name='name'),
]
