from django.shortcuts import render
from django.views.generic import TemplateView

from tempview.models import TempModel
# Create your views here.


# def index(request):
#     data = TempModel.objects.all()
#     context = {
#         'data': data,
#     }
#     return render(request, 'tempview/index.html', context)


class TempView(TemplateView):
    template_name = 'tempview/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = TempModel.objects.all()
        context['data'] = data
        return context


class TempDetailView(TemplateView):
    template_name = 'tempview/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs['id']
        data = TempModel.objects.get(id=id)
        context['data'] = data
        return context
