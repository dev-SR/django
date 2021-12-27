from django.contrib import admin
from . import models
from django.db.models import Count


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory',
                    'inventory_status_fn']
    list_editable = ['price']
    ordering = ['title']
    list_per_page = 5

    def reviews__body(self, obj):
        return obj.reviews.all()[0].body

    @admin.display(ordering='inventory')
    def inventory_status_fn(self, product):
        return 'In Stock' if product.inventory > 0 else 'Out of Stock'


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_price', 'body', 'vote']
    list_filter = ['vote']
    search_fields = ['body']
    ordering = ['created_at']
    list_per_page = 5
    # Selecting Related Objects
    list_select_related = ['product']

    def product_price(self, review):
        return review.product.price


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'products_count']
    ordering = ['name']
    list_per_page = 5

    @admin.display(ordering='products_count')
    def products_count(self, tag):
        return tag.products.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(products_count=Count('products'))
