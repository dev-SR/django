from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.core.paginator import Paginator
from django.contrib import messages

from .models import PhotoModel, Todo

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


class PhotoForm(forms.ModelForm):
    class Meta:
        model = PhotoModel
        fields = ['caption', 'image']


# https://docs.djangoproject.com/en/5.0/topics/class-based-views/mixins/#using-formmixin-with-detailview
class TodoDetailView(FormMixin, DetailView):
    model = Todo
    form_class = PhotoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        self.object = self.get_object()  # !Important as it is used in form validation process,get_success_url
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.todo = self.get_object()
        photo.save()

        messages.success(self.request, 'Photo added successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error adding photo. Please check the form.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("todo-detail", kwargs={"pk": self.object.pk})


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


def delete_photo(request, photo_id, todo_id):
    photo = get_object_or_404(PhotoModel, id=photo_id)
    photo.delete()

    todo = get_object_or_404(Todo, id=todo_id)
    context = {
        'object': todo,
    }
    return render(request, 'app/image_grid.html', context)
