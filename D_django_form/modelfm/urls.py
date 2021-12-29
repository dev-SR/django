
from django.urls import path

from . import views

urlpatterns = [
    path("", views.modelform),
    path("classbased", views.ReviewView.as_view()),
    path("thank-you", views.thank_you),
]
