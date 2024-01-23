from django.shortcuts import render
from app.models import Product, Category, Review, Tag, Order, Customer
from django.db.models import Q, F, Count, Avg, Min, Max


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


def index(request):
    print("*"*50)
    q = Customer.objects.annotate(order_count=Count('orders'))
    for customer in q:
        print(f'{customer.name} | order count: {customer.order_count}')

    print("*"*50)
    return render(request, 'index.html')
