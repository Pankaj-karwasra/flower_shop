from django.urls import path, include
from rest_framework import routers
from .views import (
    ProductViewSet, OrderViewSet, AppointmentViewSet,
    index, user_login, user_logout, admin_dashboard, customer_dashboard,
    product_list, product_detail, product_create, product_update, product_delete,
    add_to_cart, cart_detail, remove_from_cart, checkout, order_list
)
from . import views


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('customer_dashboard/', customer_dashboard, name='customer_dashboard'),
    path('api/', include(router.urls)),
    
     # Paths for managing products
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:pk>/update/', product_update, name='product_update'),
    path('products/<int:pk>/delete/', product_delete, name='product_delete'),

    # Paths for shopping cart
    path('cart/', cart_detail, name='cart_detail'),
   # path('cart/add/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    
    # Paths for checkout and orders
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_list, name='order_list'),
]