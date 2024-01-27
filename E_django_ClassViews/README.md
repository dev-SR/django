# Generic Class Views in Django

- [Generic Class Views in Django](#generic-class-views-in-django)
  - [CRUD workflow](#crud-workflow)
    - [ListView](#listview)
    - [DetailView](#detailview)
    - [CreateView](#createview)
    - [UpdateView](#updateview)
    - [DeleteView](#deleteview)
    - [Redirecting to all the views](#redirecting-to-all-the-views)
  - [Advance ListView](#advance-listview)
    - [ListView with Pagination](#listview-with-pagination)
    - [Passing extra context to the template](#passing-extra-context-to-the-template)
    - [Filtering the queryset](#filtering-the-queryset)
    - [Search and Filtering the queryset using URL parameters](#search-and-filtering-the-queryset-using-url-parameters)
    - [Dynamic search and filtering using htmx](#dynamic-search-and-filtering-using-htmx)
  - [DetailView + FormMixin/FormView](#detailview--formmixinformview)

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

Lets start with a simple model, which we will use to demonstrate the CRUD workflow. We will be using a simple todo model with the following fields:

`app/models.py`

```python
from django.db import models
class Todo(models.Model):
    title = models.CharField(max_length=200, blank=False)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

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

## Advance ListView


We can override or implement properties and methods `ListView` class to customize the view.

Doc:

- [https://ccbv.co.uk/projects/Django/5.0/django.views.generic.list/ListView/](https://ccbv.co.uk/projects/Django/5.0/django.views.generic.list/ListView/)

### ListView with Pagination

```python
from django.views.generic.list import ListView
from .models import Todo

class TodoList(ListView):
    model = Todo
    paginate_by = 10
```

In the template, we can use the `paginator` object as `page_obj` having the attributes such as `number`, `paginator`, `has_next`, `has_previous`, `has_other_pages`, `next_page_number`, `previous_page_number`, `start_index`, `end_index`, `page_range` etc.

### Passing extra context to the template

```python
from django.views.generic.list import ListView
from .models import Todo

class TodoList(ListView):
    model = Todo
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Todo List'
        return context
```

Now we can access the `title` in the template as `{{ title }}`.

### Filtering the queryset

filter by time created

```python
from django.views.generic.list import ListView
from .models import Todo
class TodoList(ListView):
    model = Todo
    paginate_by = 10

    def get_queryset(self):
        return Todo.objects.order_by('-created')
```

### Search and Filtering the queryset using URL parameters

```python

from django.views.generic.list import ListView

class TodoList(ListView):
    model = Todo
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        filter = self.request.GET.get('filter', None)
        search = self.request.GET.get('search', None)
        if filter == 'active':
            qs = qs.filter(complete=False)
        elif filter == 'complete':
            qs = qs.filter(complete=True)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs
```

In `templates\app\todo_list.html` we can add a form to filter the queryset.

```html
<!-- ... -->
<form method="get" class="flex space-x-2">
    <input type="text" name="search" id="search" class="px-2 py-1 border border-gray-700 rounded">
    <select name="filter" id="filter" class="px-2 py-1 border border-gray-700 rounded">
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="complete">Complete</option>
    </select>
    <button type="submit"
            class="px-2 py-1 bg-indigo-500 text-white rounded hover:bg-indigo-600">Filter
    </button>
    <button> type="button"
            class="px-2 py-1 bg-gray-500 text-white rounded hover:bg-gray-600"
            onclick="window.location.href = '{% url 'todo-list' %}'">Clear
    </button>
</form>
<table id="todo-list">
<!-- ... -->
</table>

```

But his will not preserve the form. To preserve the form we can use `django.forms.Form` class and pass it to the template.

```python

from django.views.generic.list import ListView
from django import forms

class TodoListForm(forms.Form):
    filter = forms.ChoiceField(choices=(('all', 'All'), ('active', 'Active'), ('complete', 'Complete')))
    search = forms.CharField(max_length=100, required=False, label='Search')

class TodoList(ListView):
    model = Todo
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        filter = self.request.GET.get('filter', None)
        search = self.request.GET.get('search', None)
        if filter == 'active':
            qs = qs.filter(complete=False)
        elif filter == 'complete':
            qs = qs.filter(complete=True)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TodoListForm(self.request.GET)
        return context
```


`templates\app\todo_list.html`

```html
<!-- ... -->
<form method="get" class="flex space-x-2">
    {% for field in form %}<div class="w-40">{{ field }}</div>{% endfor %}
    <button type="submit"
            class="px-2 py-1 bg-indigo-500 text-white rounded hover:bg-indigo-600">Filter</button>
    <button type="button"
            class="px-2 py-1 bg-gray-500 text-white rounded hover:bg-gray-600"
            onclick="window.location.href = '{% url 'todo-list' %}'">Clear</button>
</form>
<table id="todo-list">
<!-- ... -->
</table>

```

### Dynamic search and filtering using htmx

```python
class TodoList(ListView):
    model = Todo
    paginate_by = 2

    def get_queryset(self):  # exec order [2]
        qs = super().get_queryset()
        filter = self.request.GET.get('filter', None)
        search = self.request.GET.get('search', None)
        if "paginate_by" in self.request.GET:
            paginate_by = self.request.GET.get('paginate_by')
            if not paginate_by == "":
                self.paginate_by = paginate_by

        if filter == 'active':
            qs = qs.filter(complete=False)
        elif filter == 'complete':
            qs = qs.filter(complete=True)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_context_data(self, **kwargs):  # exec order [3]
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', None)
        context['filter'] = self.request.GET.get('filter', None)
        context['paginate_by'] = self.request.GET.get('paginate_by', None)
        context['search_options'] = ['all', 'active', 'complete']
        context['paginate_by_options'] = ['2', '5', '10']
        return context

    def get(self, request, **kwargs):  # exec order [1]
        isHtmx = request.headers.get('HX-Request')

        # if request is not htmx then return the default response
        if not isHtmx:
            return super().get(request, **kwargs)

        # else add custom paginated response
        qs = self.get_queryset()
        paginator = Paginator(qs, self.paginate_by)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
        }

        return render(request, 'app/todo_list_table.html', context)
```

Additional context data will be passed to populate the search and filter form as well as the pagination options according to the current state of url parameters.


`templates\app\todo_list.html`

Below we will be sending `GET` request using a `form` element but not submitting the form. Instead we will be using triggering when the user types in the search input or selects an option from the select element. This is done by `hx-trigger="keyup changed delay:250ms from:#search, change from:#filter, change from:#paginate_by"`, meaning the changes in the `#search`, `#filter` and `#paginate_by` elements will trigger the `GET` request, sending their values as parameters.

Additionally, by `hx-push-url="true"` we are telling htmx to push the url, which will help us to preserve the state of current url parameters and form values and use them query the database.

```html
<!-- ... -->
<form id="filter-form"
        hx-get="{% url 'todo-list' %}"
        hx-target="#todo-list"
        hx-trigger="keyup changed delay:250ms from:#search, change from:#filter, change from:#paginate_by"
        hx-push-url="true"
        class="flex space-x-2"
        autocomplete="off">
    <!-- Search input -->
    <input type="text"
            name="search"
            id="search"
            class="px-2 py-1 border border-gray-700 rounded"
            placeholder="Search"
            {% if search %}value="{{ search }}"{% endif %}>
    <!-- Filter select -->
    <select name="filter"
            id="filter"
            class="px-2 py-1 border border-gray-700 rounded">
        <option disabled value="" {% if filter == None %}selected{% endif %}>Filter by status</option>
        {% for option in search_options %}
            <option value="{{ option }}" {% if filter == option %}selected{% endif %}>{{ option|title }}</option>
        {% endfor %}
    </select>
    <!-- Paginate by select -->
    <select name="paginate_by"
            id="paginate_by"
            class="px-2 py-1 border border-gray-700 rounded">
        <option disabled value="" {% if paginate_by == None %}selected{% endif %}>Paginate by</option>
        {% for option in paginate_by_options %}
            <option value="{{ option }}"
                    {% if paginate_by == option %}selected{% endif %}>{{ option }}</option>
        {% endfor %}
    </select>
    <a href="{% url 'todo-list' %}"
        class="items-start w-1/3 justify-items-start underline">Refresh</a>
</form>
<div id="todo-list">
    <table class="table">

    </table>
    <!-- pagination starts -->
    <nav class="pt-4 w-full">

    </nav>
    <!-- pagination end -->
</div>
```

The dynamic htmx request will be processed by the `get()` method, which will return the `app/todo_list_table.html` template with paginated data.

`templates\app\todo_list_table.html`

```html
<table class="table">
    <!-- head -->
    <tbody>
        {% for object in page_obj %}
        {% endfor %}
    </tbody>
</table>
<!-- pagination starts -->
<nav class="pt-4 w-full">
    <ul class="flex justify-end w-full space-x-2">
        {% if page_obj.has_previous %}
            <li class="border border-gray-500 flex item-center justify-center">
                <button class="text-blue-500 py-2 px-3 cursor-pointer"
                        hx-get="{{ request.path }}?page={{ page_obj.previous_page_number }}"
                        hx-target="#todo-list"
                        hx-push-url="true"
                        hx-include="#filter-form">Prev.</button>
            </li>
        {% endif %}
        <!-- .... -->

    </ul>
</nav>
<!-- pagination end -->
```

Notice that return pagination component is different from the default pagination component. This is because once will apply search and filer the pagination should also be dynamic and should be able to preserve the state of the current url parameters and form values when we go to the next page.

To make pagination dynamic we need to add the following attributes to the pagination component.

- `hx-get="{{ request.path }}?page={{ page_obj.previous_page_number }}"`: This will send a `GET` request to the current url with the `page` parameter set to the previous page number.
- `hx-target="#todo-list"`: This will replace the content of the `#todo-list` element with the response.
- `hx-push-url="true"`: This will push the url to the browser history.
- `hx-include="#filter-form"`: This will include the `#filter-form` element in the request, which will preserve the state of the form.


## DetailView + FormMixin/FormView

Let's say we are redirecting to the detail view of product, and we want to add a review to that product. Therefore we also need to pass the form to the template.

```python
class PhotoModel(models.Model):
    caption = models.CharField(max_length=200, blank=False)
    image = models.ImageField(upload_to='images', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.caption

class PhotoForm(forms.ModelForm):
    class Meta:
        model = PhotoModel
        fields = ['caption', 'image']

# https://docs.djangoproject.com/en/5.0/topics/class-based-views/mixins/#using-formmixin-with-detailview
class TodoDetailView(FormMixin, DetailView):
    model = Todo
    form_class = PhotoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        self.object = self.get_object()  # !Important as it is used in form validation process,get_success_url
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.todo = self.get_object()
        photo.save()

        messages.success(self.request, 'Photo added successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error adding photo. Please check the form.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("todo-detail", kwargs={"pk": self.object.pk})
```

Since here we are using form to upload images the `enctype="multipart/form-data"` is required in the template.

```html
<form method="post" enctype="multipart/form-data">
    <!--  -->
</form>
```