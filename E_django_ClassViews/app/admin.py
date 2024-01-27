from django.contrib import admin
from django.utils.html import mark_safe
from .models import Todo, PhotoModel


class PhotoInline(admin.TabularInline):
    model = PhotoModel
    extra = 1


@admin.register(PhotoModel)
class PhotoModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image', 'get_thumbnail', 'todo', 'created', )
    list_filter = ('created',)
    list_display_links = ('id', 'caption')

    def get_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50"/>')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'complete')
    list_display_links = ('id', 'title')
    list_filter = ('complete',)
    inlines = [PhotoInline]
