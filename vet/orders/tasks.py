from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Querido {order.first_name},\n\n' \
              f'Tu pedido ha sido registrado exitosamente!.' \
              f'Este e stu codigo del envio {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent