from rest_framework import serializers
from .models import Category, Product, Review


class CategoryListSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    def get_product_count(self, obj):
        return obj.product_set.count()
    
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price reviews'.split()


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'