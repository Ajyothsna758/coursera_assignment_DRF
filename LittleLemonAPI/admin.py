from django.contrib import admin

# Register your models here.
from .models import MenuItem, Order, OrderItem, Cart, Category
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)