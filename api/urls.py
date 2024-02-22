from django.urls import path
from . import views

urlpatterns = [
    # category
    path('categorys/', views.category_list, name='category-list'),
    path('categorys/<str:slug>/', views.category_detail, name='category-detail'),
    # product
    path('products/', views.product_list, name='product-list'),
    path('products/<str:slug>/', views.product_detail, name='product-detail'),
    # wishlist & review
    path('wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('review/', views.add_review, name='add-review'),
    # cart_products
    path('cart-products/', views.cart_product_list, name='cart-product-list'),
    path('cart-products/<str:slug>/', views.cart_product_detail, name='cart-product-detail'),
    # carts
    path('carts-active/', views.active_carts, name='active-cart-list'),
    path('carts-inactive/', views.inactive_carts, name='inactive-cart-list'),
    path('carts/<str:slug>/', views.cart_detail, name='cart-detail'),
]




from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from main import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from openpyxl import load_workbook
from .funcs import pagenator_page, search_with_fields





# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def delete_category(request, id):
#     models.Category.objects.get(id=id).delete()
#     return redirect('dashboard:list_category')


# # Product

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def product_create(request):
#     categorys = models.Category.objects.all()
#     context = {
#         'categorys':categorys
#     }
#     if request.method == "POST":
#         name = request.POST['name']
#         description = request.POST['description']
#         quantity = request.POST['quantity']
#         price = request.POST['price']
#         currency = request.POST['currency']
#         baner_image = request.FILES['baner_image']
#         category_id = request.POST['category_id']
#         images = request.FILES.getlist('images')
#         product = models.Product.objects.create(
#             name=name,
#             description = description,
#             quantity=quantity,
#             price=price,
#             currency=currency,
#             baner_image=baner_image,
#             category_id=category_id
#         )
#         for image in images:
#             models.ProductImage.objects.create(
#                 image=image,
#                 product=product
#             )
#         return redirect('dashboard:dashboard')
#     return render(request, 'dashboard/product/create.html', context)


# # Auth
# @api_view(['POST'])
# def sign_up(request):
#     user = User.objects.create_user(
#                                 username=request.data.get('username'),  
#                                 password=request.data.get('password'),
#                                 is_staff=True,
#                                 )
#     token = Token.objects.create(user=user)
#     return Response({'token':token.key})