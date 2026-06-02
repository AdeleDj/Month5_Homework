from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategoryListSerializer, CategoryDetailSerializer
from .serializers import ProductListSerializer, ProductDetailSerializer
from .serializers import ReviewListSerializer, ReviewDetailSerializer
from django.db.models import Avg



@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewListSerializer(reviews, many=True).data
    rating = Review.objects.aggregate(avg=Avg('stars'))['avg']
    return Response(data={
        'reviews': list_,
        'rating': round(rating, 2) if rating else 0
    })


@api_view(['GET'])
def review_detail_api_view(request, id):
    review = Review.objects.get(id=id)
    data = ReviewDetailSerializer(review, many=False).data
    return Response(data=data)


@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    list_ = ProductListSerializer(products, many=True).data
    return Response(
        data=list_
    )


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            data={'error': 'Product not found!'},
            status=status.HTTP_404_NOT_FOUND
        )
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)


@api_view(['GET'])
def categories_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(
            data={'error': 'Category not found!'},
            status=status.HTTP_404_NOT_FOUND
        )
    data = CategoryDetailSerializer(category, many=False).data
    return Response(data=data)


@api_view(['GET'])
def categories_list_api_view(request):
    categories = Category.objects.all()
    list_ = CategoryListSerializer(categories, many=True).data
    return Response(
        data=list_
    )
