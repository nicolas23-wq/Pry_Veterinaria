from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),

    path('admin/order/<int:order_id>/', views.admin_order_detail,
                                        name='admin_order_detail'),
    path('historial/', views.historial_ventas_cliente, name='historial_ventas_cliente'),
    path('historial_admin/', views.historial_ventas_admin, name='historial_ventas_admin'),
]