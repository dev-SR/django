from app.models import Product
from pprint import pprint
from django.db.models import Q
from datetime import datetime, timezone


# def run(*arg):

#     # Exact Match
#     query1 = Product.objects.filter(title='Product 1')

#     # Case-Insensitive Exact Match
#     query2 = Product.objects.filter(title__iexact='product 1')

#     # Contains
#     query3 = Product.objects.filter(title__contains='Product')

#     # Case-Insensitive Contains
#     query4 = Product.objects.filter(title__icontains='product')

#     # StartsWith
#     query5 = Product.objects.filter(title__startswith='P')

#     # EndsWith
#     query6 = Product.objects.filter(title__endswith='1')

#     # In List
#     titles_list = ['Product 1', 'Product 2', 'Product 3']
#     query7 = Product.objects.filter(title__in=titles_list)

#     # Greater Than
#     query8 = Product.objects.filter(price__gt=0.00)

#     # Less Than
#     query9 = Product.objects.filter(price__lt=100000.00)

#     # Date Range
#     start_date = datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
#     end_date = datetime(2025, 12, 31, tzinfo=timezone.utc)
#     query10 = Product.objects.filter(created_at__range=(start_date, end_date))

#     # Status Filter (Choices Field)
#     query11 = Product.objects.filter(status=Product.Status.ACTIVE)

#     # Tag Filter (Many-to-Many Relationship)
#     query12 = Product.objects.filter(tags__name__icontains='Tag 1')

#     # Combining Queries with OR
#     combined_query = (query1 | query2 | query3 | query4 | query5 | query6 |
#                       query7 | query8 | query9 | query10 | query11 | query12).distinct()

#     # Combining Queries with AND
#     combined_query_and = (query1 & query8 & query11).distinct()

#     # Displaying results
#     print(list(combined_query))
#     print(list(combined_query_and))

# def run():
#     # Q objects with different filtering methods
#     # Example 1: OR conditions
#     or_conditions = Q(title__icontains='product') | Q(
#         description__icontains='good')

#     # Example 2: AND conditions
#     and_conditions = Q(price__gt=50.00) & Q(status=Product.Status.ACTIVE)

#     # Example 3: Combined OR and AND conditions
#     combined_conditions = (Q(title__icontains='product') | Q(
#         description__icontains='good')) & Q(price__gt=50.00)

#     # Example 4: Excluding certain conditions
#     exclude_condition = ~Q(status=Product.Status.INACTIVE)

#     # Applying the conditions to the queryset
#     result_or_conditions = Product.objects.filter(or_conditions)
#     result_and_conditions = Product.objects.filter(and_conditions)
#     result_combined_conditions = Product.objects.filter(combined_conditions)
#     result_exclude_condition = Product.objects.filter(exclude_condition)

#     # Displaying results
#     print(result_or_conditions)
#     print(result_and_conditions)
#     print(result_combined_conditions)
#     print(result_exclude_condition)


def run():
    def build_dynamic_query(**kwargs):
        dynamic_query = Q()

        for key, value in kwargs.items():
            if value:
                if key == 'search':
                    dynamic_query &= Q(title__icontains=value) | Q(
                        description__icontains=value)
                elif key == 'min_price':
                    dynamic_query &= Q(price__gte=value)
                elif key == 'status':
                    dynamic_query &= Q(status=value)
                # Add more conditions as needed for other parameters

        return dynamic_query

    dynamic_query = build_dynamic_query(
        search='product',
        min_price=10000,
        status='active'
        # Add more parameters as needed
    )

    products = Product.objects.filter(dynamic_query)

    print(list(products))
