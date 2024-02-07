from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormMixin,
                                       UpdateView)
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Photo, Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 5
    login_url = '/users/login/'

    def get_queryset(self):  # exec order [2]
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(owner=user)
        # default sort created by
        qs = qs.order_by('-created_at')
        if "paginate_by" in self.request.GET:
            paginate_by = self.request.GET.get('paginate_by')
            # print("1", "*"*50)
            # print(paginate_by)
            if not paginate_by == "":
                self.paginate_by = paginate_by

        search_title = self.request.GET.get('search_title', None)
        filter_creation_date = self.request.GET.get('filter_creation_date', None)
        filter_due_date = self.request.GET.get('filter_due_date', None)
        filter_priority = self.request.GET.get('filter_priority', None)
        filter_complete = self.request.GET.get('filter_complete', None)

        if search_title:
            qs = qs.filter(title__icontains=search_title)

        if filter_creation_date:
            qs = qs.filter(created_at__date=filter_creation_date)

        if filter_due_date:
            qs = qs.filter(due_date__date=filter_due_date)

        if filter_priority:
            qs = qs.filter(priority=filter_priority)

        if filter_complete:
            qs = qs.filter(is_complete=(filter_complete.lower() == 'true'))

        return qs

    def get_context_data(self, **kwargs):  # exec order [3]
        context = super().get_context_data(**kwargs)
        # context['current_page'] = self.request.GET.get('page', 1)
        return context

    def get(self, request, **kwargs):  # exec order [1]
        if 'is_dark_mode' not in request.session:  # set default theme
            request.session['is_dark_mode'] = False

        isHtmx = request.headers.get('HX-Request')

        # if request is not htmx then return the default response
        if not isHtmx:
            return super().get(request, **kwargs)

        # else add custom paginated response
        qs = self.get_queryset()
        # print("2", "*"*50)
        # print(self.paginate_by)
        paginator = Paginator(qs, per_page=self.paginate_by)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
        }

        return render(request, 'tasks/table/htmx_table.html', context)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['caption', 'image']


class TaskDetailView(LoginRequiredMixin, FormMixin, DetailView):
    login_url = '/users/login/'
    model = Task
    form_class = PhotoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # !Important as it is used in form validation process,get_success_url
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.task = self.get_object()
        photo.save()

        messages.success(self.request, 'Photo added successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error adding photo. Please check the form.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("task-detail", kwargs={"pk": self.object.pk})


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    success_url = reverse_lazy('task-list')
    login_url = '/users/login/'
    fields = ['title', 'description', 'due_date', 'priority', 'is_complete']

    def get_form(self):
        form = super().get_form()
        form.fields['due_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Associate the task with the current user
        return super().form_valid(form)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy('task-list')
    login_url = '/users/login/'
    fields = ['title', 'description', 'due_date', 'priority', 'is_complete']

    def get_form(self):
        form = super().get_form()
        form.fields['due_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Associate the task with the current user
        return super().form_valid(form)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    login_url = '/users/login/'


@login_required
def delete_photo(request, photo_id, task_id):
    photo = get_object_or_404(Photo, id=photo_id)
    photo.delete()

    task = get_object_or_404(Task, id=task_id)
    context = {
        'object': task,
    }
    return render(request, 'tasks/image_grid.html', context)
