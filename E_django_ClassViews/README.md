# Generic Class Views in Django

- [Generic Class Views in Django](#generic-class-views-in-django)
  - [TemplateView](#templateview)
    - [Showing ListView](#showing-listview)
    - [Showing DetailView](#showing-detailview)
  - [ListView](#listview)
  - [DetailView](#detailview)
  - [FormView and CreateView](#formview-and-createview)

## TemplateView

### Showing ListView

`urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tempview/', include('tempview.urls')),
]
```

`models.py`

```python
class TempModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
```

`view.py`

```python
from django.views.generic import TemplateView
from tempview.models import TempModel
# Create your views here.
# def index(request):
#     data = TempModel.objects.all()
#     context = {
#         'data': data,
#     }
#     return render(request, 'tempview/index.html', context)

class TempView(TemplateView):
    template_name = 'tempview/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = TempModel.objects.all()
        context['data'] = data
        return context
```

`index.html`

```html
<ul>
 {% for d in data %}
  <li>
   <span > <b>{{d.name}}</b> </span> - <i>{{d.email}}</i>
  </li>
 {% endfor %}
 </ul>
```

### Showing DetailView

`urls.py`

```python
from django.urls import path
from . import views
urlpatterns = [
    path('', views.TempView.as_view(), name='tempview'),
    path('<int:id>/', views.TempDetailView.as_view(), name='tempdetail'),
]
```

`view.py`

```python
class TempDetailView(TemplateView):
    template_name = 'tempview/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs['id']
        data = TempModel.objects.get(id=id)
        context['data'] = data
        return context
```

`detail.html`

```python
<body>
 <h1>{{data.name}}</h1>
 <p>{{data.email}}</p>
</body>
```

## ListView

`views.py`

```python
class ListViewClass(ListView):
    template_name = 'listview/listview.html'
    model = ModelL
    context_object_name = 'items'
    # without `context_object_name`, `object_list` is default name for list of objects
```

We can also customize :

```python
class ListViewClass(ListView):
    template_name = 'listview/listview.html'
    model = ModelL
    context_object_name = 'items'
    # without `context_object_name`, `object_list` is default name for list of objects

    #  custom query set
    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.order_by('-name')
        return data

    # customizing context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['more_info'] = 'This is more info'
        return context
```

`listveiw.html`

```html
<ul>
   {% for d in items %}
   <li>
    <span> <b>{{d.name}}</b> </span> - <i>{{d.email}}</i>
   </li>
   {% endfor %}
  </ul>

  <p>{{more_info}}</p>
```

## DetailView

> Generic detail view DetailViewClass must be called with either an object `pk` or a `slug` in the URLconf.

`urls.py`

```python
from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListViewClass.as_view(), name='listview'),
    # Generic detail view DetailViewClass must be called with either an object pk or a slug in the URLconf.
    path('<int:pk>/', views.DetailViewClass.as_view(), name='detail'),
]
```

`views.py`

```python
class DetailViewClass(DetailView):
    template_name = 'list_detail_view/detail.html'
    model = ModelL
    context_object_name = 'item'
    # without `context_object_name`, `object` is default name for object
```

`detail.html`

```html
<body>
 <h1>{{item.name}}</h1>
 <p>{{item.email}}</p>
</body>
```

## FormView and CreateView

### FormView

```python
class FormClassView(FormView):
    form_class = ReviewModelForm
    template_name = 'form_create_view/review.html'
    success_url = 'thank-you'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ThankYouView(TemplateView):
    template_name = 'form_create_view/thank_you.html'
```

### CreateView

```python
# class FormClassView(FormView):
#     form_class = ReviewModelForm
#     template_name = 'form_create_view/review.html'
#     success_url = 'thank-you'

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class CreateViewClass(CreateView):
    model = ReviewModel
    form_class = ReviewModelForm
    template_name = 'form_create_view/review.html'
    success_url = 'thank-you'
```