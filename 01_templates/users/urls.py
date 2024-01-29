
from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/',  views.CustomLoginView.as_view(), name='login'),
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),
]
