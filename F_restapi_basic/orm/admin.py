from django.contrib import admin

from .models import Category, Product, Order, OrderItem, Cart, CartItem, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "price",
        "stock",
        "category",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "created_at", "updated_at")
    search_fields = ("name",)
    date_hierarchy = "created_at"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "shipping_address",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("user", "created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity")
    list_filter = ("order", "product")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status")
    list_filter = ("user",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")
    list_filter = ("cart", "product")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "content_type",
        "object_id",
        "text",
        "rating",
    )
    list_filter = ("user", "content_type")
