from decimal import Decimal
from django.http import HttpResponseBadRequest, JsonResponse
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from orders.models import Order
from django.shortcuts import get_object_or_404
import traceback

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    # --- MENSAJES DE DEPURACIÓN EN LOGS DE RENDER ---
    print("--- INICIO DE payment_process ---")
    print(f"DEBUG: request.method: {request.method}")
    print(f"DEBUG: STRIPE_SECRET_KEY cargada: {'Sí' if settings.STRIPE_SECRET_KEY else 'No, clave vacía'}")
    print(f"DEBUG: STRIPE_PUBLISHABLE_KEY cargada: {'Sí' if settings.STRIPE_PUBLISHABLE_KEY else 'No, clave vacía'}")
    print(f"DEBUG: YOUR_DOMAIN (desde settings): {settings.YOUR_DOMAIN}")
    print(f"DEBUG: request.is_secure(): {request.is_secure()}") # Debería ser True en Render (HTTPS)
    print(f"DEBUG: request.get_host(): {request.get_host()}") # Debería ser tu dominio de Render

    order_id = request.session.get('order_id', None)
    if not order_id:
        print("ERROR: order_id no encontrado en la sesión.")
        # Podrías redirigir a una página de error o al carrito
        return HttpResponseBadRequest("No se encontró ID de orden en la sesión.")

    try:
        order = get_object_or_404(Order, id=order_id)
        print(f"DEBUG: Orden {order.id} recuperada.")
    except Exception as e:
        print(f"ERROR: No se pudo recuperar la orden {order_id}: {e}")
        traceback.print_exc()
        return HttpResponseBadRequest(f"Error al recuperar la orden: {e}")


    if request.method == 'POST':
        try:
            # Construcción de URLs absolutas (esto es correcto)
            success_url = request.build_absolute_uri(reverse('payment:completed'))
            cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

            print(f"DEBUG: success_url generada: {success_url}")
            print(f"DEBUG: cancel_url generada: {cancel_url}")

            # Stripe checkout session data
            session_data = {
                'mode': 'payment',
                'client_reference_id': str(order.id), # Convertir a string, buena práctica
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
            }

            # add order items to the Stripe checkout session
            for item in order.items.all():
                # Asegúrate de que item.price sea un Decimal o float antes de multiplicar
                # int() para convertir a centavos/unidad más pequeña
                unit_amount_cents = int(item.price * Decimal('100'))
                print(f"DEBUG: Añadiendo ítem '{item.product.name}' - Precio: {item.price}, Cantidad: {item.quantity}, Monto en centavos: {unit_amount_cents}")
                session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': unit_amount_cents,
                        'currency': 'usd', # <-- ¡IMPORTANTE! Asegúrate de que esta moneda sea correcta (ej. 'cop', 'eur')
                        'product_data': {
                            'name': item.product.name,
                            # 'images': [request.build_absolute_uri(item.product.image.url)] if item.product.image else [], # Opcional: Si tienes URLs de imagen accesibles públicamente
                        },
                    },
                    'quantity': item.quantity,
                })

            # Validar que haya line_items antes de crear la sesión
            if not session_data['line_items']:
                print("ERROR: No hay ítems en la orden para procesar en Stripe.")
                return HttpResponseBadRequest("No se encontraron ítems en la orden para el pago.")

            # create Stripe checkout session
            print("DEBUG: Llamando a stripe.checkout.Session.create()...")
            session = stripe.checkout.Session.create(**session_data)

            print(f"DEBUG: Sesión de Stripe creada con éxito. ID: {session.id}, URL: {session.url}")
            # redirect to Stripe payment form
            return redirect(session.url, code=303) # Redirección HTTP 303 (See Other)

        except stripe.error.StripeError as e:
            # Errores específicos de la API de Stripe
            print(f"ERROR STRIPE: Código: {e.code}")
            print(f"ERROR STRIPE: Mensaje Stripe: {e.user_message or e.error_message}")
            print(f"ERROR STRIPE: Parámetro: {e.param}")
            traceback.print_exc() # Imprime el traceback completo
            return JsonResponse({'error': f"Error de Stripe: {e.user_message or e.error_message}"}, status=400)
        except Exception as e:
            # Cualquier otro error inesperado (ej. de Python)
            print(f"ERROR GENERAL INESPERADO en payment_process: {e}")
            traceback.print_exc() # Imprime el traceback completo
            return JsonResponse({'error': "Un error inesperado ocurrió al procesar el pago."}, status=500)
        finally:
            print("--- FIN DE INTENTO DE PAGO (Bloque POST) ---")

    else: # Si el método no es POST (ej. GET)
        print("DEBUG: Renderizando payment/process.html (método GET).")
        return render(request, 'payment/process.html', locals())
    
        session = stripe.checkout.Session.create(**session_data) #desempaquetador pasamos los datos de la seccion kwargs
        return redirect(session.url, code=303)
        return render(request, 'payment/process.html', locals())

def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
# Create your views here.
