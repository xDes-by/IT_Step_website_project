from .models import ProductInCart


def show_cart_count(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    products = ProductInCart.objects.filter(session_key=session_key)
    product_count = sum([product.count for product in products])
    return locals()