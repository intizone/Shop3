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


