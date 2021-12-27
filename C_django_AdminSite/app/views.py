from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from .models import Book
# Create your views here.


def index(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'app/index.html', context)


def book_detail(request, s):
    # try:
    #     book = Book.objects.get(id=id)
    # except:
    #     raise Http404('Book does not exist')
    book = get_object_or_404(Book, slug=s)
    context = {
        'title': book.title,
        'author': book.author,
        'rating': book.rating,
    }
    return render(request, 'app/book_detail.html', context)
