from .models import Product
from rest_framework import serializers


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'content', 'created_at', 'updated_at', 'image', 'author']
        extra_kwargs = {
            'author': {'required': False}
        }