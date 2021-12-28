from django.urls import path
from . import views
urlpatterns = [
    path('', views.review_class, name='review_class'),
    path('thank-you', views.thank_you),
]
