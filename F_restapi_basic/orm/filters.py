import django_filters
from .models import Product


class ProductListFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
            "price": ["exact", "gte", "lte", "range"],
        }
