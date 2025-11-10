from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from . import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
#from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from random import choice


# The admin can assign users to the manager group
# You can access the manager group with an admin token
# API end point: http://127.0.0.1:8000/api/admin/users/
@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAdminUser])
def admin_manager(request):
    if request.method == "GET":
        # For GET: list all users in the “Manager” group
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        users = manager_group.user_set.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    username= request.data['username']
    if username:
        user= get_object_or_404(User, username=username)
        manager= Group.objects.get(name="Manager")
        if request.method== "POST":
            manager.user_set.add(user)
            message= f'{user} added in Manager Group'
        elif request.method== "DELETE":
            manager.user_set.remove(user) 
            message= f'{user} removed from Managers Group' 
        return Response({"message": message})  
    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)  

# to see all groups as a admin
# API end point: http://127.0.0.1:8000/api/admin/groups/
@api_view()
@permission_classes([IsAdminUser])
def admin_groups(request):
    items= Group.objects.all()
    serialized_item= serializers.GroupSerializer(items, many=True)
    return Response(serialized_item.data)

# to see all users as a admin
@api_view()
@permission_classes([IsAdminUser])
def admin_users(request):
    items= User.objects.all()
    serialized_item= serializers.UserSerializer(items, many=True)
    return Response(serialized_item.data)

# category endpoint api: 
# as a manager u can see and add (create) category items
# as a customer/ delivery-crew member u can see category (not able to add category )
# API end point: http://127.0.0.1:8000/api/category/
# class CategoryItems(ListCreateAPIView):
#     queryset= Category.objects.all()
#     serializer_class= serializers.CategorySerializer
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def category(request):
    if request.method=="GET":
        items= Category.objects.all()
        serialized_items= serializers.CategorySerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    if request.method=="POST":
        if not request.user.groups.filter(name="Manager").exists():
            return Response({"message":"you are authorized to create category because you are not manager"}, status=status.HTTP_401_UNAUTHORIZED)
        serialized_item= serializers.CategorySerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)

# as a manager u can update, delete or get the single category item
# as a customer/dc u can only view single category item (no update or delete)
# API end point: http://127.0.0.1:8000/api/category/2   {categoryid=2} 
# class SingleCategoryItem(RetrieveUpdateDestroyAPIView):
#     queryset= Category.objects.all()
#     serializer_class= serializers.CategorySerializer 
@api_view(["GET","PUT","PATCH","DELETE"])
@permission_classes([IsAuthenticated])
def single_category(request, id):
    item= get_object_or_404(Category,pk=id)
    if request.method=="GET":
        serialized_item= serializers.CategorySerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message":"You are not authorized because you are not manager"}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method=="PUT":
        serialized_item=serializers.CategorySerializer(item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_205_RESET_CONTENT)
    if request.method=="PATCH":
        serialized_item=serializers.CategorySerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_206_PARTIAL_CONTENT)
    if request.method=="DELETE":
        item.delete()
        return Response({"message":"category item deleted"}, status=status.HTTP_204_NO_CONTENT)
    
        
# Menu Item API End points:
# API end point: http://127.0.0.1:8000/api/menu-items/
# managers only able to add menu item
# all users able see all menu items list
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menuitem_view(request):
    if request.method== "GET":
        item= MenuItem.objects.select_related("category").all()
        # filter with category
        category_name= request.query_params.get("category")
        if category_name:
            item=item.filter(category__title= category_name)
        # filter with  less than given price
        price= request.query_params.get("to_price") 
        if price:
            item=item.filter(price__lte= price)  
        # search with any letter/s from menu item name
        search= request.query_params.get("search")
        if search:
            item=item.filter(title__contains=search)  
        # ordering
        ordering= request.query_params.get("ordering")
        if ordering:
            ordering_fields= ordering.split(",")
            item= item.order_by(*ordering_fields)   
        #pagination
        # perpage= request.query_params.get("perpage", default=2)
        # page= request.query_params.get("page", default=1) 
        # paginator= Paginator(item, per_page=perpage)
        # try:
        #     item= paginator.page(number=page)
        # except EmptyPage:
        #     item=[]          
        serialized_item= serializers.MenuItemSerializer(item, many=True)
        return Response(serialized_item.data)
    
    if request.method== "POST":
        if request.user.is_staff or request.user.groups.filter(name="Manager").exists():
            serialized_item= serializers.MenuItemSerializer(data= request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
    return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)
        
# Single Menu Item API endpoints:
# API end point: http://127.0.0.1:8000/api/menu-items/1
@api_view(["GET","PUT","PATCH","DELETE"])   
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def single_menuitem_view(request, pk):
    item= get_object_or_404(MenuItem, pk=pk)
    if request.method== "GET":
        serialized_item= serializers.MenuItemSerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)
    
    # if  not (request.user.is_superuser and request.user.groups.filter(name="Manager").exists()):
    #     print(request.user.is_superuser)
    #     return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)  
        
    # if request.method=="PUT":       
    #         serialized_item= serializers.MenuItemSerializer(item, data=request.data)
    #         serialized_item.is_valid(raise_exception=True)
    #         serialized_item.save()
    #         return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
            
    # if request.method== "PATCH": 
    #         serialized_item= serializers.MenuItemSerializer(item, data=request.data, partial=True)
    #         serialized_item.is_valid(raise_exception=True)
    #         serialized_item.save()
    #         return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)

    # if request.method== "DELETE": 
    #         item.delete()
    #         return Response({"message": "item deleted"}, status.HTTP_204_NO_CONTENT)  
         
    
    if request.user.is_staff or request.user.groups.filter(name="Manager").exists():
        if request.method=="PUT":
            serialized_item= serializers.MenuItemSerializer(item, data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
        if request.method== "PATCH":
            serialized_item=serializers.MenuItemSerializer(item, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
        if request.method== "DELETE":
            item.delete()
            return Response({"message": "item deleted"}, status.HTTP_204_NO_CONTENT)
    else:
        return Response({"message": "You are not authorized."}, status.HTTP_403_FORBIDDEN)    
             
# User Group Management API endpoints:
# as a manager able to read all managers list and creates or deletes user from managers Group
# API end point: http://127.0.0.1:8000/api/groups/manager/users/
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def manager_add(request):
    if  not request.user.groups.filter(name="Manager").exists():
        return Response({"message":"you are not Authorized because not manager"}, status=status.HTTP_403_FORBIDDEN)
    if request.method=="GET":
        managers= User.objects.filter(groups=Group.objects.get(name="Manager"))
        serialized_managers= serializers.UserSerializer(managers, many=True)
        return Response(serialized_managers.data)
    if request.method=="POST":
        username= request.data.get("username")
        if not username:
            return Response({"message":"username parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        user= get_object_or_404(User, username=username)
        manager= Group.objects.get(name="Manager")
        manager.user_set.add(user)
        message= f'{user} added in Manager Group'
        return Response({"message": message}, status=status.HTTP_201_CREATED)

# As a manager I am able to DELETE user from managers group
# # API end point: http://127.0.0.1:8000/api/groups/manager/users/1/   {user_id=1} 
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def manager_delete(request, pk):
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message":"you are not Authorized because not manager"}, status=status.HTTP_400_BAD_REQUEST)
        
    user= get_object_or_404(User, pk=pk)
    if user.groups.filter(name="Manager").exists():
        manager= Group.objects.get(name="Manager")
        manager.user_set.remove(user)
        message= f'{user.username} is removed from managers group'
        return Response({"message":message}, status.HTTP_200_OK)
    else:
        return Response({"message": "This user is not a manager"}, status.HTTP_404_NOT_FOUND) 
    
# Manager able to add or see delivery-crew  users
# API end point: http://127.0.0.1:8000//api/groups/delivery-crew/users
@ api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def delivery_add(request):
    if not request.user.groups.filter(name="Manager").exists():
        return Response({"message":"you are not Authorized because not manager"}, status=status.HTTP_403_FORBIDDEN)
    if request.method=="GET":
        delivery= User.objects.filter(groups=Group.objects.get(name="Delivery crew"))
        serialized_delivery= serializers.UserSerializer(delivery, many=True)
        return Response(serialized_delivery.data, status=status.HTTP_200_OK)
    if request.method== "POST":
        username= request.data.get("username")
        if not username:
            return Response({"message": "you need to provide username parameter"}, status=status.HTTP_400_BAD_REQUEST)
        user= get_object_or_404(User, username=username)
        delivery= Group.objects.get(name="Delivery crew")
        delivery.user_set.add(user)
        message= f'{user} added in Delivery crew member'
        return Response({"message":message}, status=status.HTTP_201_CREATED)

# Manager able to delete user from Delivery Crew group
# API end point: http://127.0.0.1:8000/api/groups/delivery-crew/users/9/  {userid=9}
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delivery_delete(request, pk):
    if not request.user.groups.filter(name="Manager").exists():
        if request.method=="DELETE":
            return Response({"message":"You are not authorized because not manager"}, status=status.HTTP_403_FORBIDDEN)
    if request.method=="DELETE":
        user= get_object_or_404(User, pk=pk)
        if user.groups.filter(name="Delivery crew").exists():
            delivery= Group.objects.get(name="Delivery crew")
            delivery.user_set.remove(user)
            message= f'{user.username} is removed from delivery crew group'
            return Response({"message":message}, status.HTTP_200_OK)
        else:
            return Response({"message": "This user is not a delivery crew member"}, status.HTTP_404_NOT_FOUND)

# Cart Management API endpoints:
# as a customer able to add, delete or get menu items
# API end point: http://127.0.0.1;8000/api/cart/menu-items   
@api_view(["GET","POST","DELETE"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def cart(request):
    if request.user.groups.filter(name="Manager").exists() or request.user.groups.filter(name="Delivery crew").exists():
        return Response({"message": "you are not authorized because not customer"}, status=status.HTTP_403_FORBIDDEN)
    if request.method == "GET":
        # Get all cart items for this user
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response(
                {"message": "The cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Serialize list of cart items
        serialized_items = serializers.CartSerializer(cart_items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        menuitem_id = request.data.get("menuitem")
        quantity = int(request.data.get("quantity", 1))

        menu_item = get_object_or_404(MenuItem, pk=menuitem_id)
        # Check if user already has this item in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            menuitem=menu_item,
            defaults={
                "quantity": quantity,
                "unit_price": menu_item.price,
                "price": menu_item.price * quantity
            }
        )
        if not created:
            # If item already exists, increase quantity
            cart_item.quantity += quantity
            cart_item.price = cart_item.quantity * cart_item.unit_price
            cart_item.save()

        serialized_item = serializers.CartSerializer(cart_item)
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
    if request.method=="DELETE":
        cart_items= Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"message":"your cart is already empty"}, status=status.HTTP_400_BAD_REQUEST)
        cart_items.delete()
        return Response({"message":"deleted all items from cart"}, status=status.HTTP_204_NO_CONTENT)

# Order management API end points:
# as a customer get all orders with order items created by this user
# as a manager get all orders with order items by all users
# as a dc get all orders with order items assigned to the delivery crew
# API end point: http://127.0.0.1:8000/api/orders/
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def order(request):
    if request.method=="GET":
        # for manager
        if request.user.groups.filter(name="Manager").exists() or request.user.is_staff:
            items= Order.objects.all()
            # filter with price
            price= request.query_params.get("to_price")
            if price:
                items= items.filter(total__lte=price)
            # search with status
            search= request.query_params.get("search")
            if search:
                items= items.filter(status__icontains=search) 
            # ordering with fields
            ordering= request.query_params.get("ordering")
            if ordering:
                order_fields= ordering.split(",")
                items= items.order_by(*order_fields)       
            # pagination
            perpage= request.query_params.get("perpage", default=2)
            page= request.query_params.get("page", default=1)
            paginator= Paginator(items,per_page=perpage)
            try:
                    items=paginator.page(number=page)
            except EmptyPage:
                    items=[]     
            serialized_items= serializers.OrderSerializer(items, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK) 
        # for delivery crew
        elif request.user.groups.filter(name="Delivery crew").exists():
            items= Order.objects.filter(delivery_crew=request.user)
            serialized_item= serializers.OrderSerializer(items, many=True)
            return Response(serialized_item.data, status=status.HTTP_200_OK)
        # for customer
        else:
            if Order.objects.filter(user=request.user).exists():
                items= Order.objects.filter(user=request.user)
                serialized_item= serializers.OrderSerializer(items, many=True)
                return Response(serialized_item.data, status=status.HTTP_200_OK) 
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method== "POST":
        # check for not manager/dc/admin
        if request.user.groups.filter(name__in=["Manager", "Delivery crew"]).exists() or request.user.is_staff:
            return Response({"message":"You are not authorized to create order because you are not customer"}, status=status.HTTP_401_UNAUTHORIZED)
        # for customers
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        
        if not cart_items.exists():
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_order_price = 0
        order_items = []

        # Create OrderItems for each cart item
        for item in cart_items:
            order_item_data = {
                "user_id": user.id,
                "menuitem_id": item.menuitem.id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "price": item.price
            }
            serializer = serializers.OrderItemSerializer(data=order_item_data)
            serializer.is_valid(raise_exception=True)
            order_item = serializer.save()
            order_items.append(order_item)
            total_order_price += item.price

        # Create the Order
        delivery_crew_members=User.objects.filter(groups__name="Delivery crew")
        delivery_crew_user= choice(delivery_crew_members) if delivery_crew_members.exists() else None        
        order_data = {
            "user_id": user.id,
            "total": total_order_price,
            "status": False,  
            "orderitem_id": order_items[0].id,
            "delivery_crew": delivery_crew_user.id if delivery_crew_user else None
            
            
        }
        order_serializer = serializers.OrderSerializer(data=order_data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()
        # Delete the cart items
        cart_items.delete()
        return Response({"message": "Order is created"}, status=status.HTTP_201_CREATED)

# As a user able to see or get order details
# As a manager able to update(PUT or PATCH) or deletes order
# As a delivery crew member able to partially update (PATCH) the status of order
# API endpoint: http://127.0.0.1:8000/api/orders/1 {orderid=1}
@api_view(["GET","PUT","PATCH","DELETE"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def single_order(request, pk):
    item= get_object_or_404(Order, pk=pk)
    if request.method=="GET":
        if item.user!= request.user:
            return Response({"message":"You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        serialized_item= serializers.OrderSerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)
    
    if request.method=="PUT":
        if not request.user.groups.filter(name="Manager").exists():
            return Response({"message":"you are not authorized because you are not manager"}, status=status.HTTP_401_UNAUTHORIZED)
        serialized_item= serializers.OrderSerializer(item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_205_RESET_CONTENT)
    
    if request.method=="DELETE":
        if not request.user.groups.filter(name="Manager").exists():
            return Response({"message":"you are not authorized to delete this order because you are not manager"}, status=status.HTTP_401_UNAUTHORIZED)
        item.delete()
        return Response({"message": "item deleted"}, status.HTTP_204_NO_CONTENT)
    
    if request.method=="PATCH":
        if request.user.groups.filter(name="Manager").exists():
            serialized_item= serializers.OrderSerializer(item, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status=status.HTTP_206_PARTIAL_CONTENT)
        if request.user.groups.filter(name="Delivery crew").exists():
            if item.delivery_crew!= request.user:
                return Response({"message":"you are not authorized to update"}, status=status.HTTP_403_FORBIDDEN)
            #only able to update status
            status_data={"status":request.data.get("status", item.status)}
            serialized_item= serializers.OrderSerializer(item, data=status_data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
        return Response({"message": "You are not authorized to update this order"},status=status.HTTP_403_FORBIDDEN)
        
        
            
        
        
                
              
            
            
    
         
        
        
          

    
        
             
        
              
        
        
        

