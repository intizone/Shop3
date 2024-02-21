from . import views
from django.urls import path

app_name = 'dashboard'

urlpatterns = [
    # dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Category
    path('categorys_count', views.categorys_count, name='categorys_count'),
    path('list_category', views.list_category, name='list_category'),
    path('create_category', views.create_category, name='create_category'),
    path('detail_category/<str:slug>', views.detail_category, name='detail_category'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    
    # Product
    path('product_create', views.product_create, name='product_create'),
    path('product_list', views.product_list, name='product_list'),
    path('product_update/<int:id>', views.product_update, name='product_update'),
    path('product_detail/<str:slug>', views.product_detail, name='product_detail'),
    path('product_delete/<int:id>', views.product_delete, name='product_delete'),
    
    # excel down_s
    path('print_to_excel/', views.print_to_excel, name='print_to_excel'),
    path('excel/', views.excel, name='excel'),
    path('download_excel/', views.download_excel, name='download_excel'),
    path('download_excels/<int:id>/', views.download_excels, name='download_excels'),

    # auth
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('user_update', views.user_update, name='user_update'),
    
    # enter
    path('enter-list/', views.list_enter, name='list_enter'),
    path('enter-create/', views.create_enter, name='create_enter'),
    path('enter-update/<int:id>/', views.update_enter, name='update_enter'),
    path('enter-delete/<int:id>/', views.delete_enter, name='delete_enter'),
    path('enters-delete/<int:id>/', views.delete_enters, name='delete_enters'),
    
    # search 
    path('search_view/', views.search_view, name='search_view'),
]