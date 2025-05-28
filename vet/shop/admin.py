from django.contrib import admin
from .models import Category, Product, CustomerInfo

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price',"stock", 'available', 'created', 'updated')
    actions = ['generar_pedido_automatico']
    def low_stock_alert(self, obj):
        if obj.is_low_stock():
            return "¡Stock bajo!"
        return ""
    low_stock_alert.short_description = "Alerta de Stock"
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    def generar_pedido_automatico(self, request, queryset):
        pedidos = 0
        for product in queryset:
            if product.is_low_stock():
                orden = product.generar_pedido_automatico()
                if orden:
                    pedidos += 1
        self.message_user(request, f"Se generaron {pedidos} pedidos automáticos para productos con stock bajo.")
    generar_pedido_automatico.short_description = "Generar pedido automático a proveedor para stock bajo"
    
@admin.register(CustomerInfo)
class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'email', 'created']
    search_fields = ['nombre', 'apellido', 'email']
    

admin.site.site_header = "Veterinaria Admin"
admin.site.site_title = "Veterinaria Admin Portal"
admin.site.index_title = "Bienvenido al portal de administración de Veterinaria"
# Register your models here.
