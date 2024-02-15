from django.contrib import admin
from .models import Category, Product, Option, Attribute, ProductVariant, VariantOption, VariantAttribute


class VariantOptionInline(admin.TabularInline):
    model = VariantOption
    extra = 1
    autocomplete_fields = ('option',)
    can_delete = True


class VariantAttributeInline(admin.TabularInline):
    model = VariantAttribute
    extra = 1
    autocomplete_fields = ('attribute',)
    can_delete = True


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    autocomplete_fields = ('product',)
    can_delete = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'price',
        'image',
        'category',
        'created_at',
        'updated_at',
    )
    list_filter = ('category', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    inlines = [
        ProductVariantInline,

    ]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'computed_variant_name', 'sku', 'price', 'stock')
    list_display_links = ('id', 'computed_variant_name', 'sku')
    autocomplete_fields = ('product',)
    inlines = [
        VariantOptionInline,
        VariantAttributeInline,
    ]

    readonly_fields = ('computed_variant_name',)  # Add the computed field here
    ordering = ('-product',)

    def computed_variant_name(self, obj):
        return obj.variant_name()  # Call the variant_name method of the ProductVariant object

    computed_variant_name.short_description = 'Variant Name'  # Customize the column header in the admin interface


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    list_filter = ('parent',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'computed_values')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

    def computed_values(self, obj):
        obj.variant_options.all()
        values = []
        for vo in obj.variant_options.all():
            values.append(vo.value)
        return ', '.join(list(set(values)))

    computed_values.short_description = 'Values'


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
