from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from core.models import BaseModel


class Product(models.Model):
    title = models.CharField(
        max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Status(models.TextChoices):
        # first value is stored in db and second value is displayed in admin
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE)

    tags = models.ManyToManyField("Tag", related_name="products")

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


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
