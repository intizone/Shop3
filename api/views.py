from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from main.models import Product, Cart, Category
from .serializers import *
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate


# category views functions
@api_view(['GET'])
def category_list(request):
    categorys = Category.objects.all()
    serializer = CategoryListSerializer(categorys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_detail(request, slug):
    try:
        category = Category.objects.get(slug = slug)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)


# product views functions
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


# wishlist views function
@api_view(['POST'])
def add_to_wishlist(request):
    serializer = WishListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# review views function
@api_view(['POST'])
def add_review(request):
    serializer = ProductReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# cart views functions
@api_view(['GET'])
def active_carts(request):
    carts = Cart.objects.filter(is_active=True)
    serializer = CartSerializer(carts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def inactive_carts(request):
    carts = Cart.objects.filter(is_active=False)
    serializer = CartSerializer(carts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def cart_detail(request, slug):
    try:
        cart = Cart.objects.get(slug=slug)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# cart_product views functions
@api_view(['GET', 'POST'])
def cart_product_list(request):
    if request.method == 'GET':
        cart_products = CartProduct.objects.all()
        serializer = CartProductSerializer(cart_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CartProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def cart_product_detail(request, slug):
    try:
        cart_product = CartProduct.objects.get(slug=slug)
    except CartProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CartProductSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CartProductSerializer(cart_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        cart_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)