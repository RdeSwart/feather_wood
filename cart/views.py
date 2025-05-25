from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


def cart(request):
    """
    This view returns the Shopping Cart Page
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id, item_data in cart.items():
        product = get_object_or_404(Product, pk=item_id)

        quantity = item_data.get('quantity', 0)
        subtotal = item_data.get('subtotal', float(product.rrp_price) * quantity)
        total += subtotal

        cart_items.append({
            'item_id': item_id,
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    delivery = 6.99
    grand_total = total + delivery

    context = {
        'cart_items': cart_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return render(request, 'cart.html', context)


def add_to_cart(request, item_id):
    """ Add a quantity of the product to the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    print("CART DATA:", cart)

    item_id = str(item_id)
    if item_id in cart:
        cart[item_id]['quantity'] += quantity
        cart[item_id]['subtotal'] = float(cart[item_id]['quantity'] *
                                          product.rrp_price)
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]["quantity"]}')
    else:
        cart[item_id] = {
            'quantity': quantity,
            'subtotal': float(product.rrp_price * quantity)
        }
        messages.success(request, f'Added {product.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """ Adjust the quantity of the product to the shopping cart """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    item_id = str(item_id)
    cart = request.session.get('cart', {})

    if quantity > 0:
        subtotal = float(quantity * product.rrp_price)
        cart[item_id] = {'quantity': quantity, 'subtotal': subtotal}
        messages.success(
            request, f'Updated {product.name} quantity to {cart[item_id]["quantity"]}')
    else:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your Cart')

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, item_id):
    """ Remove the item from the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})
    if item_id in cart:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your Cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
