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


# def run():
#     def build_dynamic_query(**kwargs):
#         dynamic_query = Q()

#         for key, value in kwargs.items():
#             if value:
#                 if key == 'search':
#                     dynamic_query &= Q(title__icontains=value) | Q(
#                         description__icontains=value)
#                 elif key == 'min_price':
#                     dynamic_query &= Q(price__gte=value)
#                 elif key == 'status':
#                     dynamic_query &= Q(status=value)
#                 # Add more conditions as needed for other parameters

#         return dynamic_query

#     dynamic_query = build_dynamic_query(
#         search='product',
#         min_price=10000,
#         status='active'
#         # Add more parameters as needed
#     )

#     products = Product.objects.filter(dynamic_query)

#     print(list(products))
from faker import Faker
from faker_commerce import Provider as CommerceProvider
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.utils import DataError
from app.models import Product, Tag, Review, Attribute, ProductAttribute, Category


def run():
    fake = Faker()
    fake.add_provider(CommerceProvider)

    print("Deleting all products, tags, and reviews")
    Category.objects.all().delete()
    Review.objects.all().delete()
    ProductAttribute.objects.all().delete()
    Attribute.objects.all().delete()
    Product.objects.all().delete()
    Tag.objects.all().delete()
    categories = ["Smartphone", 'Book', 'Computer', 'Clothing']
    tags = ["New", "Sale", "Trending", "Popular", "Best Seller"]

    print("Creating new products with reviews and tags")
    for _ in range(20):
        try:
            # Get or create category
            category, _ = Category.objects.get_or_create(
                name=fake.random.choice(categories))

            # Create Product
            product = Product(
                title=fake.ecommerce_name(),
                description=fake.sentence(nb_words=20),
                price=fake.random_int(min=100, max=1000),
                category=category,
                status=fake.random.choice(
                    [Product.Status.ACTIVE, Product.Status.INACTIVE]),
                stoke=fake.random_int(min=0, max=100)
            )
            product.save()
            # Create Reviews
            reviews = [Review(
                product=product,
                body=fake.paragraph(nb_sentences=3),
                rating=fake.random_int(min=1, max=5)
            ) for _ in range(fake.random_int(min=1, max=3))]
            Review.objects.bulk_create(reviews)

            # Create Tags
            tags = [Tag(name=tag) for tag in fake.random_choices(
                elements=tags, length=len(tags))]

            Tag.objects.bulk_create(tags)
            product.tags.set(tags)

            # Create Attributes
            attributes = [Attribute(name=fake.word())
                          for _ in range(fake.random_int(min=1, max=3))]
            Attribute.objects.bulk_create(attributes)

            # Create ProductAttributes
            product_attributes = [ProductAttribute(
                product=product,
                attribute=attribute,
                value=fake.word()
            ) for attribute in attributes]

            ProductAttribute.objects.bulk_create(product_attributes)

            print(
                f"Saved {product.title} with {len(tags)} tags and {len(reviews)} reviews.")
        except (ValidationError, IntegrityError, DataError) as e:
            print(f"Error creating product: {e}")


# # Run the function
# run()

# def run():
#     # Create a Product
#     product = Product.objects.create(
#         title="Sample Product 1",
#         description="A sample product description.",
#         price=99.99,
#         status=Product.Status.ACTIVE
#     )

#     # Create multiple Attributes
#     attributes_data = [
#         {'name': 'Color'},
#         {'name': 'Size'},
#         {'name': 'Weight'},
#     ]

#     # Create Attribute instances
#     attributes_instances = [Attribute.objects.create(
#         **attribute_data) for attribute_data in attributes_data]

#     # Associate the Attributes with the Product using the ProductAttribute intermediate table
#     for attribute_instance in attributes_instances:
#         ProductAttribute.objects.create(
#             product=product, attribute=attribute_instance, value="Sample Value")

#     # Print information
#     print(f"Product created: {product}")
#     print("Attributes associated with the product:")
#     for product_attribute in product.product_attributes.all():
#         print(f"Attribute: {product_attribute.attribute.name}")


# def run():
