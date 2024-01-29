from django.shortcuts import render

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def change_theme(request: HttpRequest):
    if "is_dark_mode" in request.session:
        request.session["is_dark_mode"] = not request.session["is_dark_mode"]
    else:
        request.session["is_dark_mode"] = False

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
def index(request):
    v = 10
    print(v)
    return render(request, 'index.html')
