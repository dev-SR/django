
from django.urls import include, path
from . import views
from .api import views as ApiViews

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('users/login/',  views.CustomLoginView.as_view(), name='login'),
    path('users/register/', views.CustomRegisterView.as_view(), name='register'),
    path('users/logout/', LogoutView.as_view(next_page="login"), name='logout'),
    path("api/users/register/", ApiViews.RegisterAPIView.as_view(), name="register-api"),
    path("api/users/login/", ApiViews.LoginAPIView.as_view(), name="login-api"),
]
