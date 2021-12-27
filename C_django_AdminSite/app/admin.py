from django.contrib import admin

# Register your models here.
# from .models import Author
# from app.models import Author
# admin.site.register(Author)

from . import models

admin.site.register(models.Product)
admin.site.register(models.Review)
admin.site.register(models.Tag)
admin.site.register(models.Book)
admin.site.register(models.Author)
