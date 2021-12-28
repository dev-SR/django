from django.shortcuts import render
from django.http import HttpResponse

from app.forms import DjangoForm


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


def render_forms(request):
    form = DjangoForm()
    return render(request, 'app/forms.html', {'form': form})
