
from django.urls import path

from . import views

urlpatterns = [
    path("", views.FormClassView.as_view(), name='formview'),
    path("create", views.FormClassView.as_view()),
    path('thank-you', views.ThankYouView.as_view()),
]
