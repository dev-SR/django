from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.variants.count()} variants"


class Option(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField()

    def __str__(self):
        computed_name = ' / '.join([f'{vo.value}' for vo in self.variant_options.all()])
        # if no variants exits append "base product"
        if not computed_name:
            computed_name = "[base product]"
        return f"{self.product.name} " + computed_name + f" ${round(self.price)}"

    def variant_name(self):
        computed_name = ' / '.join([f'{vo.value}' for vo in self.variant_options.all()])
        # if no variants exits append "base product"
        if not computed_name:
            computed_name = "[base product]"
        return f"{self.product.name} " + computed_name + f" ${round(self.price)}"


class VariantOption(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='variant_options')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.variant} - {self.option.name} - {self.value}"

    class Meta:
        unique_together = ['variant', 'option', 'value']


class VariantAttribute(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='variant_attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.variant} - {self.attribute.name} - {self.value}"
