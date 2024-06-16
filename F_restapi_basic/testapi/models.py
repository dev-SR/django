from django.db import models


class Child(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Parent(models.Model):
    name = models.CharField(max_length=20)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='parents')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products', blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.text
