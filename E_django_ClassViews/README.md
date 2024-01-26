# Generic Class Views in Django

- [Generic Class Views in Django](#generic-class-views-in-django)
  - [CRUD workflow](#crud-workflow)
    - [ListView](#listview)
    - [DetailView](#detailview)
    - [CreateView](#createview)
    - [UpdateView](#updateview)
    - [DeleteView](#deleteview)
    - [Redirecting to all the views](#redirecting-to-all-the-views)

**CBVs, or class-based views**, align with object-oriented principles, representing view calls through classes. They offer advantages such as straightforward extensibility and code reuse, simplifying complex tasks compared to FBVs (function-based views).

Django provides several built-in class-based views (CBVs) that facilitate common tasks. Here are some of them with brief descriptions:

1. **View:** The base class for all views. It handles HTTP methods through specific methods (get(), post(), etc.). It is a generic class that you can use as a base for your views.
2. **TemplateView:** Renders a template. It is commonly used for static pages where you just want to display a template without performing any specific data processing.
3. **RedirectView:** Redirects to a specific URL. Useful for simple redirects without much additional logic.

**Perform CRUD (Create, Retrieve, Update, Delete) Using Class Based Views:**
In this section, we will elaborate on the execution of Django Class-based Views. CRUD is an acronym that stands for Create, Retrieve, Update and Delete. Let us describe what each of these means.

1. **CreateView**: Create or add new entries to a database table.
2. **ListView**: To display multiple instances of a database table or to display a particular instance of a database table.
3. **DetailView:** To displays one instance of a table from the database.
4. **UpdateView**: Update or modify existing database entries in a table.
5. **DeleteView**: Remove a particular instance in a database table.
6. **FormView**: Render a form to a template and handle user data.

The structure of a simple function-based view that is used to process both GET and POST requests might look like this:

```python
# views.py
def simple_function_based_view(request):
    if request.method == 'GET':
        ...  # code to process a GET request
    elif request.method == 'POST':
        ...  # code to process a POST request
```

The same thing with a class-based view could look like this:

```python
# views.py
from django.views import View

class SimpleClassBasedView(View):
    def get(self, request):
        ...  # code to process a GET request

    def post(self, request):
        ...  # code to process a POST request
```

**Hooking up class-based views in the `urls.py` file is a little different too:**

```python
# urls.py
from . import views

urlconfig = [
    url('function/', views.simple_function_based_view),
    # the `as_view` method is called on the class-based view
    url('class/', views.SimpleClassBasedView.as_view()),
]
```

## CRUD workflow

- [https://www.dennisivy.com/django-class-based-views](https://www.dennisivy.com/django-class-based-views)
- [https://ccbv.co.uk/](https://ccbv.co.uk/)

`app/models.py`

```python
from django.db import models
class Todo(models.Model):
    title = models.CharField(max_length=200, blank=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

### ListView

1. Define a ListView

Defining a ListView is very simple. You just need to specify the model that the view will be based on.

`app\views.py`

```python
from django.views.generic.list import ListView
from .models import Todo

class TodoList(ListView):
    model = Todo
    # context_object_name = 'todo_list'
    # template_name = 'todo_list.html'
```

2. Hook up the view in the `urls.py` file:

```python

from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoList.as_view(), name='todo-list'),
]
```

3. Create a template:

By default the ListView Looks for a template with the prefix of the model name (`todo`) and the suffix of `_list.html` if not otherwise set (`todo_list.html`). The template will be passed a variable called `object_list` that will contain the list of objects retrieved from the database, which could be overridden by setting the `“context_object_name”` attribute.

So, let’s create a template called `todo_list.html` in the `templates/app` directory:

```html
<!-- .. -->
<tbody>
{% for object in object_list %}
    <tr>
        <td>{{ forloop.counter }}</td>
        <td>
            {% if object.complete == True %}
                <strike>{{ object.title }}</strike>
            {% else %}
                <span>{{ object.title }}</span>
            {% endif %}
        </td>
    </tr>
{% empty %}
    <tr>
        <td></td>
        <td>No objects yet.</td>
        <td></td>
    </tr>
{% endfor %}
</tbody>
<!-- ... -->
```

### DetailView

1. Define a DetailView

```python
from django.views.generic.detail import DetailView
from .models import Todo

class TodoDetailView(DetailView):
    model = Todo
    # context_object_name = 'todo'
    # template_name = 'todo_detail.html'
```

2. Hook up the view in the `urls.py` file:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoList.as_view(), name='todo-list'),
    path('todo/<pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
]
```

3. Create a template:

By default the DetailView looks for a template with the prefix of the model name (`todo`) and the suffix of `_detail.html` if not otherwise set (`todo_detail.html`). This can be overridden by setting the `“template_name”` attribute. The template will be passed a variable called `object` that will contain the object retrieved from the database, which could be overridden by setting the `“context_object_name”` attribute.

`todo_detail.html`

```html
{% if object.complete == True %}
    <h2 class="text-2xl font-bold">
        <strike>{{ object.title }}</strike>
    </h2>
{% else %}
    <h2 class="text-2xl font-bold">{{ object.title }}</h2>
{% endif %}
<a href="{% url 'todo-list' %}" class="underline text-indigo-500">Back to list</a>
```

### CreateView

1. Define a CreateView

```python
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class CreateTodoView(CreateView):
    model = Todo
    fields = '__all__'
    success_url = reverse_lazy('todo-list')
```

It's

2. Hook up the view in the `urls.py` file:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoList.as_view(), name='todo-list'),
    path('create/', views.CreateTodoView.as_view(), name='todo-create'),
    path('todo/<pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
]
```


- `template_name`: By default CreateView looks for a template with the prefix of the model name (`todo`) and the suffix of `_form.html` if not otherwise set (`todo_form.html`). This can be overridden by setting the `“template_name”` attribute.

- `fields`: We can specify the fields we want to use in our form by setting the `“fields”` attribute. If we don’t set this attribute, all the fields will be used.

- `success_url`: We can set the `“success_url”` attribute to redirect the user to a different page once the form is submitted. In this case, we are redirecting the user to the `“todo-list”` page.

- `form_class`: By default this view creates a model form for us based on the model we specify. As you can see in the example if we don’t specify a model form to use, one will be created by fail for us after we specify the field names. We can use our own model form by creating a mode for and setting the `“form_class attribute”`.

3. Create a template:

`templates\app\todo_form.html`

```html
{% extends "_base.html" %}
{% block content %}
    <main class="flex flex-col items-center  min-h-screen">
        <form method="post" class="flex flex-col space-y-2 w-1/3">
            {% csrf_token %}
            {% for field in form %}
                {% if field.field.widget.input_type == 'checkbox' %}
                    <div class="flex flex-row items-center space-x-2">
                        {{ field }}
                        <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                    </div>
                {% else %}
                    <div class="flex flex-col items-start w-full">
                        {{ field.label_tag }}
                        {{ field }}
                    </div>
                {% endif %}
                <div class="text-red-500">{{ field.errors }}</div>
            {% endfor %}
            <button type="submit"
                    class="py-2 px-4 rounded-md bg-indigo-500 text-white hover:bg-indigo-600 ">Submit</button>
        </form>
    </main>
{% endblock content %}
```

### UpdateView

1. Define a UpdateView

```python
from django.views.generic.edit import CreateView, UpdateView
class UpdateTodoView(UpdateView):
    model = Todo
    fields = '__all__'
    success_url = reverse_lazy('todo-list')
```

2. Hook up the view in the `urls.py` file:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoList.as_view(), name='todo-list'),
    path('create/', views.CreateTodoView.as_view(), name='todo-create'),
    path('todo/<pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
    path('todo/<pk>/update/', views.UpdateTodoView.as_view(), name='todo-update'),
]
```

3. Create a template:

This view by default follows the same template_naming convention and form principles as the create view. Both views will look for the same form and template unless otherwise specified.

### DeleteView

```python
from django.views.generic.edit import CreateView, UpdateView, DeleteView
class DeleteTodoView(DeleteView):
    model = Todo
    success_url = reverse_lazy('todo-list')
```

2. Hook up the view in the `urls.py` file:

```python

from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoList.as_view(), name='todo-list'),
    path('create/', views.CreateTodoView.as_view(), name='todo-create'),
    path('todo/<pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
    path('todo/<pk>/update/', views.UpdateTodoView.as_view(), name='todo-update'),
    path('todo/<pk>/delete/', views.DeleteTodoView.as_view(), name='todo-delete'),
]
```

3. Create a template:

`template_name`: By default DeleteView look’s for a template with the prefix of the model name (`todo`) and the suffix of `_confirm_delete.html` if not otherwise set (`todo_confirm_delete.html`). This can be overridden by setting the `“template_name”` attribute.


`templates\app\todo_confirm_delete.html`

```html
{% extends "_base.html" %}
{% block content %}
    <main class="flex flex-col items-center min-h-screen">
        <form method="post"
              action=""
              class="flex flex-col items-center space-y-4 mt-8 border border-gray-700 rounded shadow p-4">
            {% csrf_token %}
            <p>Are you sure you want to delete "{{ object }}"?</p>
            <div class="flex w-full justify-end space-x-2">
                <a href="{% url 'todo-list' %}"
                   class="px-2 py-1 bg-gray-700 text-white rounded hover:bg-gray-600">Cancel</a>
                <input type="submit"
                       value="Confirm"
                       class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600">
            </div>
        </form>
    </main>
{% endblock content %}
```

### Redirecting to all the views

`templates\app\todo_list.html`

```html
{% for object in object_list %}
    <tr>
        <td>{{ forloop.counter }}</td>
        <td>
            {% if object.complete == True %}
                <strike>{{ object.title }}</strike>
            {% else %}
                <span>{{ object.title }}</span>
            {% endif %}
        </td>
        <td>
            <div class="flex space-x-2">
                <a href="{% url 'todo-detail' object.id %}">View</a>
                <a href="{% url 'todo-update' object.id %}">Update</a>
                <a href="{% url 'todo-delete' object.id %}">Delete</a>
            </div>
        </td>
    </tr>
{% empty %}
    <tr>
        <td></td>
        <td>No objects yet.</td>
        <td></td>
    </tr>
{% endfor %}
```
