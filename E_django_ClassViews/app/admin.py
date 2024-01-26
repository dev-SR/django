from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'complete')
    list_display_links = ('id', 'title')
    list_filter = ('complete',)
