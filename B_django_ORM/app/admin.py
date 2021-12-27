from django.contrib import admin

# Register your models here.
from .models import Author, Product, Review, Tag, Book
# from app.models import Product, Review, Tags

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(Author)
