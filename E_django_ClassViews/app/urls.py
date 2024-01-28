
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoList.as_view(), name='todo-list'),
    path('create/', views.CreateTodoView.as_view(), name='todo-create'),
    path('todo/<pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
    path('todo/<pk>/update/', views.UpdateTodoView.as_view(), name='todo-update'),
    path('todo/<pk>/delete/', views.DeleteTodoView.as_view(), name='todo-delete'),
    path('delete_photo/<int:photo_id>/<int:todo_id>/', views.delete_photo, name='delete-photo'),

]
