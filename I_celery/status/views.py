from django.shortcuts import render

from .tasks import send_status


def check_status(request):
    context = {}
    send_status.delay("payload")

    return render(request, 'index.html', context)
