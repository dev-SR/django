from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from .forms import ReviewModelForm
from .models import ReviewModel
# Create your views here.
from django.views.generic import FormView, CreateView

# class ReviewView(View):
#     def get(self, request):
#         form = ReviewModelForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'form_create_view/review.html', context)

#     def post(self, request):
#         form = ReviewModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('thank-you')
#         context = {
#             'form': form
#         }
#         return render(request, 'form_create_view/thank_you.html', context)

# FormView vs CreateView

# FormView:


class FormClassView(FormView):
    form_class = ReviewModelForm
    template_name = 'form_create_view/review.html'
    success_url = 'thank-you'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# CreateView:


class CreateViewClass(CreateView):
    model = ReviewModel
    form_class = ReviewModelForm
    template_name = 'form_create_view/review.html'
    success_url = 'thank-you'


class ThankYouView(TemplateView):
    template_name = 'form_create_view/thank_you.html'
