from django.db import models
import uuid

# Create your models here.


class Product(models.Model):
    """
    Product model
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# One `Product` can have Many `Reviews`
# One `Review` can only belong to one `Product`


class Review(models.Model):
    VOTE_CHOICES = (
        ('up', 'UP VOTE'),
        ('down', 'DOWN VOTE'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES, default='up')
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)

    def __str__(self):
        return self.body[:20]
