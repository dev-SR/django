from django.contrib import admin

from .models import Todo, PhotoModel


@admin.register(PhotoModel)
class PhotoModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image', 'created', 'todo')
    list_filter = ('created',)
    list_display_links = ('id', 'caption')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'complete')
    list_display_links = ('id', 'title')
    list_filter = ('complete',)
