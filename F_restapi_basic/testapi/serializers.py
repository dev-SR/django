from rest_framework import serializers
from .models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['category'] = CategorySerializer(instance.category).data
    #     response['tags'] = TagSerializer(instance.tags, many=True).data
    #     response['tags_count'] = instance.tags.count()
    #     return response
