from django.db import models
import uuid
from django.urls import reverse
from django.utils.text import slugify
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
    tags = models.ManyToManyField('Tags', blank=True, related_name='tags')
    # 1. Tags` instead of Tag because Tag Model is defined later
    # 2. related_name='tags' is used to avoid naming convention
    #    when we access the tags from Product model
    #    i.e. instead of product.tags_set.all(),we can use product.tags.all()
    #       p = Product.objects.first()
    #       p.tags.all()

    def __str__(self):
        return self.title

# 1 to M: Product to Review
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


# M to M: Product to Tag
# Many `Products` can have Many `Tags`
# Many `Tags` can be applied to Many `Products`

class Tags(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    products = models.ManyToManyField(
        Product, blank=True, related_name='products')
    # Many to Many relation can be defined in either one of the models.
    # Or both of them for admin interface.
    # t = Tags.objects.first()
    # t.products.all()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)
    author = models.CharField(max_length=200)
    is_bestseller = models.BooleanField(default=False)
    slug = models.SlugField(default="", null=False, blank=False, db_index=True)

    # slugify before save()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # Model Url
    # def get_absolute_url(self):
    #     # return reverse('book-details', kwargs={'pk': self.pk})
    #     return reverse('book-details', args=[self.pk])
    def get_absolute_url(self):
        return reverse('book-details', args=[self.slug])

    def __str__(self):
        return self.title.title()
