from django.urls import path, re_path
from .views import (
    CustomObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    CustomProviderAuthView,
    LogoutAPIView,
)

urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),
    path("jwt/create/", CustomObtainPairView.as_view()),
    path("jwt/refresh/", CustomTokenRefreshView.as_view()),
    path("jwt/verify/", CustomTokenVerifyView.as_view()),
    path("logout", LogoutAPIView.as_view()),
]
