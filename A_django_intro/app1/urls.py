from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='app1'),
    path('id/<int:no>', views.dynamic_int, name='by_id'),
    path('name/<str:name>', views.dynamic_str, name='by_name'),
    path('any/<any1>/x/<any2>', views.dynamic_any, name='any'),
]
