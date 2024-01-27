from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from .models import Todo

from django import forms


# class TodoListForm(forms.Form):
#     search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search'}))
#     filter = forms.ChoiceField(choices=(('all', 'All'), ('active', 'Active'), ('complete', 'Complete')))
#     paginate_by = forms.ChoiceField(choices=(('2', '2'), ('5', '5'), ('10', '10')))


class TodoList(ListView):
    model = Todo
    paginate_by = 2

    def get_queryset(self):  # exec order [2]
        qs = super().get_queryset()
        filter = self.request.GET.get('filter', None)
        search = self.request.GET.get('search', None)
        if "paginate_by" in self.request.GET:
            paginate_by = self.request.GET.get('paginate_by')
            if not paginate_by == "":
                self.paginate_by = paginate_by

        if filter == 'active':
            qs = qs.filter(complete=False)
        elif filter == 'complete':
            qs = qs.filter(complete=True)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_context_data(self, **kwargs):  # exec order [3]
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', None)
        context['filter'] = self.request.GET.get('filter', None)
        context['paginate_by'] = self.request.GET.get('paginate_by', None)
        context['search_options'] = ['all', 'active', 'complete']
        context['paginate_by_options'] = ['2', '5', '10']
        return context

    def get(self, request, **kwargs):  # exec order [1]
        isHtmx = request.headers.get('HX-Request')

        # if request is not htmx then return the default response
        if not isHtmx:
            return super().get(request, **kwargs)

        # else add custom paginated response
        qs = self.get_queryset()
        paginator = Paginator(qs, self.paginate_by)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
        }

        return render(request, 'app/todo_list_table.html', context)


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
