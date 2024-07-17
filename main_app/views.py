from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Product, Order, Appointment,Cart, CartItem
from .serializers import ProductSerializer, OrderSerializer, AppointmentSerializer
from .forms import ProductForm
from django.db import IntegrityError

def index(request):
    return render(request, 'main_app/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            return render(request, 'main_app/login.html', {'error': 'Invalid login credentials'})
    return render(request, 'main_app/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('customer_dashboard')  # Redirect non-admin users
    return render(request, 'main_app/admin_dashboard.html')

@login_required
def customer_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')  # Redirect admin users
    return render(request, 'main_app/customer_dashboard.html')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'main_app/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main_app/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'main_app/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'main_app/product_form.html', {'form': form, 'product': product})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'main_app/product_confirm_delete.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Create or update cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'main_app/cart_detail.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity
            )
        cart_items.delete()
        return redirect('order_list')
    return render(request, 'main_app/checkout.html', {'cart_items': cart_items})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'main_app/order_list.html', {'orders': orders})
