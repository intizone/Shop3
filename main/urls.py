from . import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    
    # dashboard
    path('', views.index, name='index'),
    path('product/<int:id>', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    
    # cart
    path('carts', views.carts, name='carts'),
    path('cart_detail', views.cart_detail, name='cart_detail'),
    path('cart/detail/delete/', views.cart_detail_delete, name='cart_detail_delete'),
    path('cart_sale/<int:id>', views.cart_sale, name='cart_sale'),
    path('cart_create/<int:id>/', views.cart_create, name='cart_create'),
    
    # wish list
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_wish/<int:id>', views.add_wish, name='add_wish'),
    path('del_wish/<int:id>', views.del_wish, name='del_wish'),
]
