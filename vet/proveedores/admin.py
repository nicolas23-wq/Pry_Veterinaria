from django.contrib import admin
from .models import Proveedor, ProductoProveedor, OrdenCompra, DetalleOrdenCompra
# from shop.models import Product

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contacto', 'email', 'activo']
    search_fields = ['nombre', 'contacto', 'email']

@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'proveedor', 'precio', 'stock']
    search_fields = ['nombre', 'proveedor__nombre']

class DetalleOrdenCompraInline(admin.StackedInline):
    model = DetalleOrdenCompra
    extra = 0

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'fecha_orden', 'estado', 'total']
    list_filter = ['estado', 'proveedor']
    inlines = [DetalleOrdenCompraInline]
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        orden = form.instance
        # Solo actualizar stock si la orden está marcada como recibida
        if orden.estado == 'recibida':
            for detalle in orden.detalles.all():
                # Aquí puedes agregar la lógica para actualizar el stock si es necesario
                producto = detalle.producto
                producto.stock += detalle.cantidad
                producto.save()
# Register your models here.
