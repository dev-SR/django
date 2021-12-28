# Form in Django

## Handle Form Manually

`urls.py`

```python
from django.urls import path
from . import views
urlpatterns = [
    path('', views.review, name='review'),
    path('thank-you/', views.thank_you),
]
```

`views.py`

```python
def review(request):
    if request.method == 'POST':
        username = request.POST['username']
        # print(username)
        if username == '' and len(username) <= 4:
            return render(request, 'reviews/review.html', {'has_error': True})
        return HttpResponseRedirect('thank-you')

    return render(request, 'reviews/review.html')

def thank_you(request):
    return render(request, 'reviews/thank_you.html')
```

`review.html`

```html
<form method="post" action="{% url 'review' %}">
   {% csrf_token %}
   {% if has_error %}
    <p>Please enter valid user name</p>
   {% endif %}
   <label for="username">Your Username</label>
   <input type="text" name='username' id='username'>
   <button>Send</button>
</form>
```

## Handle Form with Django Form Class

`app/forms.py`

```python
from django import forms
class ReviewForm(forms.Form):
    username = forms.CharField()
```

`app/views.py`

```python
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .forms import ReviewForm

def review_class(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     # print(username)
    #     if username == '' and len(username) <= 4:
    #         return render(request, 'reviews/review.html', {'has_error': True})
    #     return HttpResponseRedirect('thank-you')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponseRedirect('thank-you')
    else:
        form = ReviewForm()

    return render(request, 'reviews_class/review.html', {'form': form})

def thank_you(request):
    return render(request, 'reviews_class/thank_you.html')
```

`review.html`

```html
<form action="{% url 'review_class' %}" method="post">
   {% csrf_token %}
   {{form}}
   <!--
   {% if has_error %}
    <p>Please enter valid user name</p>
   {% endif %}
   <label for="username">Your Username</label>
   <input type="text" name='username' id='username'>
   <label for="pass"></label>
   <input type="text" name='pass' id='pass'>
         -->
   <button type='submit'>Send</button>
  </form>
```

### Customizing the Form Controls

```python
class ReviewForm(forms.Form):
    username = forms.CharField(label="Your Username", max_length=10, error_messages={
        'required': 'Please enter your username',
        'max_length': 'Please enter a username less than 10 characters',
    })
```

### Customizing the Rendered HTML

`app/forms.py`

```python
from django import forms
class ReviewForm(forms.Form):
    username = forms.CharField(label="Your Username", max_length=10, error_messages={
        'required': 'Please enter your username',
        'max_length': 'Please enter a username less than 10 characters',
    }, required=False)
    review_text = forms.CharField(
        label="Your Review", max_length=200, widget=forms.Textarea)
    rating = forms.IntegerField(label="Your Rating", min_value=1, max_value=5)
```

`review.html`

```html
<form action="{% url 'review_class' %}" method="post">
   {% csrf_token %}
   {% for field in form %}
    <div>
     {% if field.errors %}
      errors
     {% endif %}
     {{field.label_tag}}
     {{field}}
     {{field.errors}}
    </div>
   {% endfor %}
   <button type='submit'>Send</button>
  </form>
```