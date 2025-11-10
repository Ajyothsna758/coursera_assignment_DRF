from django.urls import path
from . import views

urlpatterns=[
    path("admin/users/", views.admin_manager),
    path("admin/groups/", views.admin_groups),
    path("admin/users-list/", views.admin_users),
    path("category/", views.category),
    path("category/<int:id>/", views.single_category),
    path("menu-items/", views.menuitem_view),
    path("menu-items/<int:pk>/", views.single_menuitem_view),
    path("groups/manager/users/", views.manager_add),
    path("groups/manager/users/<int:pk>/", views.manager_delete),
    path("groups/delivery-crew/users/", views.delivery_add),
    path("groups/delivery-crew/users/<int:pk>/", views.delivery_delete),
    path("cart/menu-items/", views.cart),
    path("orders/", views.order),
    path("orders/<int:pk>/", views.single_order),
]