from django.urls import path

from .views import index, search

urlpatterns = [
    path("", index, name="todos"),
    path('search', search, name='search'),  # new

]
