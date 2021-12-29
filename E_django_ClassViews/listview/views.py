from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.
from .models import ModelL


class ListViewClass(ListView):
    template_name = 'listview/listview.html'
    model = ModelL
    context_object_name = 'items'
    # without `context_object_name`, `object_list` is default name for list of objects

	#  custom query set
    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.order_by('-name')
        return data

	# customizing context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['more_info'] = 'This is more info'
        return context
