from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields=["id", "title", "slug"]
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    category= CategorySerializer(read_only=True)
    category_id= serializers.IntegerField(write_only=True)
    class Meta:
        model=MenuItem
        fields=["id", "title","price", "featured", "category", "category_id"]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=["name"]

class UserSerializer(serializers.ModelSerializer):
    groups= GroupSerializer(read_only=True, many=True)
    class Meta:
        model=User
        fields=["id", "username", "email","groups"]

# class CartSerializer(serializers.ModelSerializer):
#     user=UserSerializer(read_only=True)
#     user_id= serializers.IntegerField(write_only=True)
#     menuitem= MenuItemSerializer(read_only=True)
#     menuitem_id= serializers.IntegerField(write_only=True)
#     unit_price= serializers.DecimalField(source="menuitem.price", max_digits=6, decimal_places=2)
#     price= serializers.SerializerMethodField(method_name="calculate_price")
#     class Meta:
#         model= Cart
#         fields=["id", "quantity","unit_price", "price","user", "user_id", "menuitem", "menuitem_id"]
#     def calculate_price(self, obj):
#         return obj.quantity * obj.menuitem.price          

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    # Make unit_price read-only (no `source="menuitem.price"` for write)
    unit_price = serializers.DecimalField(max_digits=6,decimal_places=2,read_only=True)
    price = serializers.SerializerMethodField(method_name="calculate_price")

    class Meta:
        model = Cart
        fields = ["id","quantity","unit_price","price","user","user_id","menuitem","menuitem_id",]

    def calculate_price(self, obj):
        return obj.quantity * obj.menuitem.price

    def create(self, validated_data):
        # extract write_only fields
        user_id = validated_data.pop("user_id")
        menuitem_id = validated_data.pop("menuitem_id")
        quantity = validated_data.get("quantity")
        user = User.objects.get(pk=user_id)
        menuitem = MenuItem.objects.get(pk=menuitem_id)
        # compute unit_price and price
        unit_price = menuitem.price
        total_price = unit_price * quantity
        # create instance
        cart = Cart.objects.create(user=user,menuitem=menuitem,quantity=quantity,unit_price=unit_price,price=total_price)
        return cart    
class OrderItemSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    user_id= serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price','user']


class OrderSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    user_id=serializers.IntegerField(write_only=True)
    orderitem= OrderItemSerializer(read_only=True)
    orderitem_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=Order
        fields=["id", "user", "user_id", "orderitem", "orderitem_id", "status", "delivery_crew", "total", "date"]        
        
              