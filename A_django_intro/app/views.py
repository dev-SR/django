from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, ~/app/")


def dynamic(reqest, x):
    return HttpResponse("Hello, ~/app/others/{}".format(x))
