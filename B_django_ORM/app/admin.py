from django.contrib import admin

from .models import Product, Tag, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'price',
        'created_at',
        'updated_at',
        'status',
    )
    list_display_links = ['id', 'title',]
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ['id', 'name',]
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'body',
        'rating',
        'created_at',
        'updated_at',
    )
    list_display_links = ['id',
                          'product',
                          'body',]
    list_filter = ('product', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
