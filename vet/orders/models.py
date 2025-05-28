from django.db import models
from shop.models import Product
from django.contrib.auth import get_user_model
from django.conf import settings


class Order(models.Model):
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    email = models.EmailField()
    Dirrecion = models.CharField(max_length=250)
    Codigo_postal = models.CharField(max_length=20)
    Ciudad = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']), #optimizar la velocidad de las consultas
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):  
        return sum(item.get_cost() for item in self.items.all())
    
    def get_stripe_url(self):
        if not self.stripe_id:
            # no payment associated
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for test payments
            path = '/test/'
        else:
            # Stripe path for real payments
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


    @staticmethod
    def get_user_order_history(user):
        return Order.objects.filter(user=user).order_by('-created')

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id) #metodo magico donde se retorna el id del objeto

    def get_cost(self):
        return self.price * self.quantity

# Create your models here.