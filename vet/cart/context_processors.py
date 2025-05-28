from .cart import Cart

def cart(request):
    cart = Cart(request) # Initialize the cart
    return {
        'cart': cart,
        'cart_total_price': cart.get_total_price(),
    }