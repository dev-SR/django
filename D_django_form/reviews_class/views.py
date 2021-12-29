from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from .forms import ReviewForm
from .models import Review
# Create your views here.


def review_class(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     # print(username)
    #     if username == '' and len(username) <= 4:
    #         return render(request, 'reviews/review.html', {'has_error': True})
    #     return HttpResponseRedirect('thank-you')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            review = Review(
                username=form.cleaned_data['username'],
                review_text=form.cleaned_data['review_text'],
                rating=form.cleaned_data['rating']
            )
            review.save()
            return HttpResponseRedirect('thank-you')
    else:
        form = ReviewForm()
    context = {
        'form': form
    }
    return render(request, 'reviews_class/review.html', context)


def thank_you(request):
    return render(request, 'reviews_class/thank_you.html')
