from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import ReviewModelForm
from .models import ReviewModel
# Create your views here.


def modelform(request):
    if request.method == 'POST':
        form = ReviewModelForm(request.POST)
        if form.is_valid():
            form.save()
            # print(form.cleaned_data)
            # review = ReviewModel(
            #     username=form.cleaned_data['username'],
            #     review_text=form.cleaned_data['review_text'],
            #     rating=form.cleaned_data['rating']
            # )
            # review.save()
            return HttpResponseRedirect('thank-you')
    else:
        form = ReviewModelForm()
    context = {
        'form': form
    }
    return render(request, 'modelfm/modelform.html', context)


def thank_you(request):
    return render(request, 'modelfm/thank_you.html')


class ReviewView(View):
    def get(self, request):
        form = ReviewModelForm()
        context = {
            'form': form
        }
        return render(request, 'modelfm/modelform.html', context)

    def post(self, request):
        form = ReviewModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('thank-you')
        context = {
            'form': form
        }
        return render(request, 'modelfm/modelform.html', context)
