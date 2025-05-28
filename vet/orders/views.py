from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required  # accede a esta vista solo en el modo administrador
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from .models import Order
from django import forms

class ConsultaHistorialForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")

def historial_ventas_cliente(request):
    ordenes = None
    if request.method == 'POST':
        form = ConsultaHistorialForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            ordenes = Order.objects.filter(email=email).order_by('-created')
    else:
        form = ConsultaHistorialForm()
    return render(request, 'orders/order/historial_clientes.html', {'form': form, 'ordenes': ordenes})

@staff_member_required
def historial_ventas_admin(request):
    ordenes = Order.objects.all().order_by('-created')
    return render(request, 'orders/historial_admin.html', {'ordenes': ordenes})



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
                product = item['product']
                product.stock -= item['quantity'] # Reduce stock
                if product.stock < 0:
                    product.stock = 0
                product.save()
            cart.clear()
            order_created.delay(order.id)  # Send e-mail task
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process')) # Redirect to payment
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
    

@staff_member_required #vista solo para el modulo administrativo
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order":order})

# Create your views here.
