from main.models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer



# Product serializers
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductListSerializer(serializers.ModelSerializer):
    is_discount = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    review = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'currency', 'is_discount', 'is_active', 'review']

class ProductDetailSerializer(ModelSerializer):
    is_discount = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    review = serializers.FloatField(read_only=True)
    images = ProductImageSerializer(source='productimage_set', many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'quantity', 'price', 'currency', 'discount_price', 'baner_image', 'category', 'is_discount', 'is_active', 'review', 'images']


# Category serializers
class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_products(self, obj):
        products = Product.objects.filter(category=obj)
        serializer = ProductListSerializer(products, many=True)
        return serializer.data


# wishlist serializer
class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['user', 'product']

    def create(self, validated_data):
        user = validated_data['user']
        product = validated_data['product']
                
        if WishList.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("This product is already in the wishlist.")
                
        wishlist = WishList.objects.create(user=user, product=product)
        return wishlist

    def delete(self, instance):
        instance.delete()


# review serializer
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['user', 'product', 'mark']

    def create(self, validated_data):
        user = validated_data['user']
        product = validated_data['product']
        mark = validated_data['mark']

        # Check if the user already rated the product
        review, created = ProductReview.objects.get_or_create(user=user, product=product)

        # Update the mark if the user already rated, otherwise create a new review
        if not created:
            review.mark = mark
            review.save()

        return review


# cart serializer
class CartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'is_active', 'quantity', 'total_price', 'products']

    def get_products(self, obj):
        cart_products = CartProduct.objects.filter(cart=obj)
        serializer = CartProductSerializer(cart_products, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()


# cart_product serializer
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'

    def create(self, validated_data):
        return CartProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()


