from django.db import models
from django.contrib.auth.models import User
from functools import reduce
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(' ', '-').lower()
        super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.SmallIntegerField(
        choices=(
            (1,'Dollar'), 
            (2, 'So`m')
            )
    ) 
    discount_price = models.DecimalField(
        decimal_places=2, 
        max_digits=10, 
        blank=True, 
        null=True
        )
    baner_image = models.ImageField(upload_to='baner/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    @property
    def review(self):
        reviews = ProductReview.objects.filter(product_id=self.id)
        result = reduce(lambda result, x: result +x, reviews, 0)
        try:
            result = result / reviews.count()
        except ZeroDivisionError:
            result = 0
        return result
    
    @property 
    def is_discount(self):
        if self.discount_price is None:
            return 0
        return self.discount_price > 0
    
    @property 
    def is_active(self):
        return self.quantity > 0

    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(' ', '-').lower()
        super(Product, self).save(*args, **kwargs)

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        self.slug = self.product.slug
        super(ProductImage, self).save(*args, **kwargs)

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.product.slug
        super(WishList, self).save(*args, **kwargs)
    
def check_duplicate_wishlist(sender, instance, **kwargs):
    if WishList.objects.filter(user=instance.user, product=instance.product).exists():
        raise ValidationError("This product is already in the wishlist.")
models.signals.pre_save.connect(check_duplicate_wishlist, sender=WishList)


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mark = models.SmallIntegerField()

    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        self.slug = self.product.slug
        super(ProductReview, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        self.slug = self.user.username
        super(Cart, self).save(*args, **kwargs)

    @property
    def quantity(self):
        quantity = 0
        products = CartProduct.objects.filter(product_id = self.id)
        for i in products:
            quantity +=i.quantity
        return quantity

    @property
    def total_price(self):
        result = 0
        for i in CartProduct.objects.filter(card_id=self.id):
            result +=(i.product.price)*i.quantity
        return result


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        self.slug = self.product.slug
        super(CartProduct, self).save(*args, **kwargs)

    @property
    def total_price(self):
        if self.product.is_discount:
            result = self.product.discount_price * self.quantity
        else:
            result = self.product.price * self.quantity
        return result


class EnterProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    quantity_enter_notation = models.SmallIntegerField(
        choices=(
            (0,'Ayrish'), 
            (1, 'Qo`shish')
        ), 
        default=0
    )
    is_active = models.BooleanField(default=False) 
    slug = models.SlugField(blank=True)
    def __str__(self):
        return f"{self.quantity} {self.product_name}"
    
    slug = models.SlugField(blank=True)
    def save(self, *args, **kwargs):
        self.slug = self.product.slug
        super(EnterProduct, self).save(*args, **kwargs)
        
    
    def save(self, *args, **kwargs):
        self.product_name = self.product.name
        if self.pk:
            enter = EnterProduct.objects.get(pk=self.pk)
            product = enter.product
            if enter.quantity_enter_notation == 0:  # Ayrish
                product.quantity -= enter.quantity
                product.quantity += self.quantity
            else:
                product.quantity += self.quantity
            product.save()
        else:
            if self.quantity_enter_notation == 0:  # Ayrish
                self.product.quantity -= self.quantity
            else:
                self.product.quantity += self.quantity
            self.product.save()
        super(EnterProduct, self).save(*args, **kwargs)
