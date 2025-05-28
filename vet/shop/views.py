from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, CustomerInfo
from cart.forms import CartAddProductForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def save_customer_info(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        # Guardar en la base de datos
        CustomerInfo.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email
        )
        messages.success(request, "¡Datos guardados correctamente!")
        # Redirige a la página de inicio
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')
        
        
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})

# Create your views here.
