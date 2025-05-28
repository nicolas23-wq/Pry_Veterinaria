from django.db import models
from django.urls import reverse
from proveedores.models import OrdenCompra, DetalleOrdenCompra, Proveedor

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    LOW_STOCK_THRESHOLD = 5
    available = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name_plural = 'Products'
        verbose_name = 'Product'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    def is_low_stock(self):
        return self.stock <= self.LOW_STOCK_THRESHOLD
    def generar_pedido_automatico(self, cantidad=10):
        proveedor = Proveedor.objects.filter(activo=True).first()  # Elige el proveedor adecuado
        if proveedor:
            orden = OrdenCompra.objects.create(proveedor=proveedor, estado='pendiente')
            DetalleOrdenCompra.objects.create(
                orden=orden,
                producto=self,
                cantidad=cantidad,
                precio_unitario=self.price
            )
            return orden
        return None
    
class CustomerInfo(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Customer Info'
        verbose_name_plural = 'Customer Infos'
        indexes = [
            models.Index(fields=['apellido', 'nombre']),
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

# Create your models here.
