from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods  # new

from .todo import todos  # new


def index(request):
    # modified
    return render(request, 'todos/index.html', {'todos': todos[:10]})


@require_http_methods(['POST'])
def search(request):
    res_todos = []
    search = request.POST['search']
    if len(search) == 0:
        return render(request, 'todos/todo.html', {'todos': todos[:10]})
    for i in todos:
        if search in i['title']:
            res_todos.append(i)
    return render(request, 'todos/todo.html', {'todos': res_todos})
