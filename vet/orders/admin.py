from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_payment(obj):
    url = obj.get_stripe_url() #crea urls para que se muestre en stripe
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>' #especie de hipervinculo 
        return mark_safe(html) #evitar hackers
    return ''

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response) #creamos archivos csv 
    fields = [field for field in opts.get_fields() if not \
              field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id]) #GENERA DINAMICAMENTE APARTIR DE LA URL
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'


export_to_csv.short_description = 'Export to CSV'

order_payment.short_description = 'Stripe payment'


class OrderItemInline(admin.TabularInline): #ajuste de visualizacion dentro de la consola
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'Nombre', 'Apellido', 'email', 'Dirrecion', 'Codigo_postal', 'Ciudad', "paid", order_payment, 'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
# Register your models here.
