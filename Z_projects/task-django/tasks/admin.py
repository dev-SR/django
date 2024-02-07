# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Task, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    min_num = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'truncated_title',
        'truncated_description',
        'due_date',
        'priority',
        'is_complete',
        'owner',
        'created_at',
        'updated_at',
    )
    list_display_links = ('id', 'truncated_title')
    list_filter = (
        'due_date',
        'is_complete',
        'owner',
        'created_at',
        'updated_at',
    )
    search_fields = ('title', 'description')
    inlines = [PhotoInline]
    ordering = ('priority',)
    autocomplete_fields = ('owner',)

    def truncated_description(self, obj):
        return obj.description[:10] + '...' if len(obj.description) > 10 else obj.description

    truncated_description.short_description = 'Description'

    def truncated_title(self, obj):
        return obj.title[:10] + '...' if len(obj.title) > 10 else obj.title

    truncated_title.short_description = 'Title'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'caption',
        'image',
        'task',
        'created_at',
        'updated_at',
    )
    list_display_links = ('id', 'caption')
    list_filter = ('task', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('task',)
