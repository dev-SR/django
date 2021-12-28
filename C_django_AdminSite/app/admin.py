from django.contrib import admin, messages
from django.contrib.admin.decorators import action
from . import models
from django.db.models import Count


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return (
            ('in', 'In Stock'),
            ('out', 'Out of Stock'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'in':
            return queryset.filter(inventory__gt=0)
        if self.value() == 'out':
            return queryset.filter(inventory=0)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title', 'price', 'inventory',
                    'inventory_status_fn']
    list_editable = ['price']
    ordering = ['title']
    list_per_page = 5
    search_fields = ['title__icontains']
    list_filter = [InventoryFilter]

    def reviews__body(self, obj):
        return obj.reviews.all()[0].body

    @admin.display(ordering='inventory')
    def inventory_status_fn(self, product):
        return 'In Stock' if product.inventory > 0 else 'Out of Stock'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        cleared_inventory = queryset.update(inventory=0)
        self.message_user(
            request, f'Cleared {cleared_inventory} inventory', messages.ERROR)


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_price', 'body', 'vote']
    list_filter = ['vote']
    search_fields = ['body']
    ordering = ['created_at']
    list_per_page = 5
    # Selecting Related Objects
    list_select_related = ['product']
    list_filter = ['product', 'vote']

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
