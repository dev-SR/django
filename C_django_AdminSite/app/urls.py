from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path("books/<slug:s>", views.book_detail, name='book-details'),
]
