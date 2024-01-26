from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Todo


class TodoList(ListView):
    model = Todo
    paginate_by = 2


class TodoDetailView(DetailView):
    model = Todo


class CreateTodoView(CreateView):
    model = Todo
    fields = '__all__'
    success_url = reverse_lazy('todo-list')


class UpdateTodoView(UpdateView):
    model = Todo
    fields = '__all__'
    success_url = reverse_lazy('todo-list')


class DeleteTodoView(DeleteView):
    model = Todo
    success_url = reverse_lazy('todo-list')
