from django.db import models
from django.conf import settings

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class ProductoProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.proveedor.nombre})"

class OrdenCompra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]
    proveedor = models.ForeignKey(Proveedor, related_name='ordenes', on_delete=models.CASCADE)
    fecha_orden = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.proveedor.nombre}"

    def calcular_total(self):
        total = sum([item.get_subtotal() for item in self.detalles.all()])
        self.total = total
        self.save()

    def recibir_orden(self):
        for detalle in self.detalles.all():
            detalle.producto.stock += detalle.cantidad
            detalle.producto.save()
        self.estado = 'recibida'
        self.save()

class DetalleOrdenCompra(models.Model):
    orden = models.ForeignKey("OrdenCompra", related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.name} x {self.cantidad}"

# Create your models here.
