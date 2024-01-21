from django.contrib import admin

from .models import Product, Tag, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'price',
        'created_at',
        'updated_at',
        'status',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'body',
        'rating',
        'created_at',
        'updated_at',
    )
    list_filter = ('product', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
