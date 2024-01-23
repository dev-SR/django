from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from core.models import BaseModel


class Category (models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Status(models.TextChoices):
        # first value is stored in db and second value is displayed in admin
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE)

    tags = models.ManyToManyField(
        "Tag", related_name="products")

    attributes = models.ManyToManyField(
        "Attribute", related_name="products", through="ProductAttribute")

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f'{self.title}'


class Review(models.Model):
    '''Model definition for Review.'''
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name='reviews')
    body = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.body[:20]}...'


class Attribute(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return f'{self.name}'
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_attributes")
    attribute = models.ForeignKey(
        "Attribute", on_delete=models.CASCADE, related_name="product_attributes")
    value = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="orders")
    payment_method = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} | {self.payment_method} | {self.created_at.strftime('%d-%m-%Y')}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.title}'
