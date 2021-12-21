from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'languages': ['Python', 'Java', 'C++', 'C#', 'JavaScript']
    }

    return render(request, 'app/index.html', context)


def dynamic(request, x):
    context = {
        'value': x
    }
    return render(request, 'app/dynamic.html', context)
