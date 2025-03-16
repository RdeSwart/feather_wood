from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal


def cart_contents(request):

    cart_items = []
    total = Decimal('0.00')
    product_count = 0
    delivery = Decimal('6.99')
    cart = request.session.get('cart', {})

    for item_id, item_data in cart.items():

        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += Decimal(item_data) * product.rrp_price
            product_count += item_data
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })

        else:
            product = get_object_or_404(Product, pk=item_id)
            quantity = item_data['quantity']
            total += quantity * product.rrp_price
            product_count += quantity
            cart_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
            })

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
