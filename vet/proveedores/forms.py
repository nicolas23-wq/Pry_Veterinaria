from django import forms
from .models import Proveedor, ProductoProveedor, OrdenCompra, DetalleOrdenCompra

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'direccion', 'email', 'telefono', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductoProveedorForm(forms.ModelForm):
    class Meta:
        model = ProductoProveedor
        fields = ['proveedor', 'nombre', 'descripcion', 'precio', 'stock']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'notas']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DetalleOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }