from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse

students_data = [
    {
        "id": 1,
        "name": "Jhon",
    },
    {
        "id": 2,
        "name": "Doe",
    },
    {
        "id": 3,
        "name": "Jane",
    },
    {
        "id": 4,
        "name": "Dane",
    },

]


def index(request):
    context = {
        "name": "dhaka university",
        "students": students_data,
        "isOpen": True,
    }

    return render(request, 'app1/index.html', context)


def dynamic_any(request, any1, any2):
    return JsonResponse({
        "any1": any1,
        "any2": any2
    })


def dynamic_int(request, no):
    try:
        student = students_data[no - 1]
        return JsonResponse(student)
    except Exception:
        return HttpResponse("No student found")


def dynamic_str(request, name):
    return HttpResponse(name)
