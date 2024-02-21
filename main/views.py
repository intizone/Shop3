from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import models
from django.db.models import Q


def index(request):
    q = request.GET.get('q')
    if q:
        products = models.Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else: 
        products = models.Product.objects.filter(quantity__gt=0)
    categorys = models.Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id:
        products.filter(category_id=category_id)
        
    wishs = models.WishList.objects.all()
    wish_ids = []
    for obj in wishs:
        product = models.Product.objects.get(id=obj.product.id)
        wish_ids.append(product.id)
    print(wish_ids)
    context = {
        'products':products,
        'categorys':categorys,
        'wish_ids':wish_ids
    }
    return render(request, 'index.html', context)

def contact(request):
    return render(request, 'contact.html')


def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    categorys = models.Category.objects.all()
    recomendation = models.Product.objects.filter(
        category_id=product.category.id).exclude(id=product.id)[:3]
    images = models.ProductImage.objects.filter(product_id=product.id)
    try:
        wish = models.WishList.objects.get(user=request.user, product=product)
        res = wish.id
    except:
        res = 0

    context = {
        'product':product,
        'categorys':categorys,
        'recomendation':recomendation,
        'images':images,
        'range':range(product.review),
        'res':res
    }
    return render(request, 'product/detail.html', context)


def cart_create(request, id):
    is_active_cart = models.Cart.objects.filter(is_active=True, user=request.user)
    
    if not is_active_cart:
        models.Cart.objects.create(
            user = request.user
        )
        try:
            product = models.Product.objects.get(id=id)
            cart = models.Cart.objects.get(is_active=True, user=request.user)
            models.CartProduct.objects.create(
                card = cart,
                product = product
            )
        except:
            pass
    else:
        cart = models.Cart.objects.get(is_active=True, user=request.user)
        item = models.Product.objects.get(id=id)
        try:
            product = models.CartProduct.objects.get(product = item, cart=cart)
            product.quantity += 1
            product.save()
        except:            
            models.CartProduct.objects.create(
                cart = cart,
                product = item
            ) 
    return redirect('main:index')


def carts(request):
    active = models.Cart.objects.filter(is_active=True, user=request.user)
    in_active = models.Cart.objects.filter(is_active=False, user=request.user)
    context = {
        'active':active,
        'in_active':in_active
    }
    return render(request, 'cart/carts.html', context)


def cart_sale(request, id):
    cart = models.Cart.objects.get(id=id, is_active=True)
    cart_products = models.CartProduct.objects.filter(cart=cart)
    for cart_product in cart_products:
        if cart_product.product.quantity >= cart_product.quantity:
            product = cart_product.product
            product.quantity -= cart_product.quantity
            product.save()

        else:
            return HttpResponse("Maxsulot etarli emas")
    cart.is_active = not cart.is_active
    cart.save()

    return redirect('main:index')

def cart_detail(request):
    try:
        cart = models.Cart.objects.get(is_active=True, user=request.user)
        items = models.CartProduct.objects.filter(cart=cart)
        
        context = {
            'cart': cart,
            'items': items
        }
    except:
        return HttpResponse("Sizga hali produclar yo`q")        
    return render(request, 'cart/cart_detail.html', context)

def cart_detail_delete(request):
    item_id = request.GET['items_id']
    item = models.CartProduct.objects.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1  
        item.save()      
    else:
        item.delete()
    
    try:
        return redirect('main:cart_detail')
    except:
        return redirect('main:index')
        
        
def wishlist(request):
    items = models.WishList.objects.filter(user=request.user)
    return render(request, 'wishlist/index.html', {'items':items})


def add_wish(requset, id):
    user = requset.user
    product = models.Product.objects.get(id=id)
    try:
        models.WishList.objects.create(
            user=user,
            product=product
        )
    except:
        pass
    return redirect('main:wishlist')


def del_wish(requset, id):
    product = models.Product.objects.get(id=id)
    user = requset.user
    wish = models.WishList.objects.get(user=user, product=product).delete()
    return redirect('main:wishlist')
