from django.contrib import admin

# Register your models here.
from .models import Product, Review, Tags, Book
# from app.models import Product, Review, Tags

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Tags)
admin.site.register(Book)
