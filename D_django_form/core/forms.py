from django import forms
from app.models import Category, Product, Tag


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'tags']
        exclude = ['description']
