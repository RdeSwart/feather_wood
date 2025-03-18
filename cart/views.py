from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


def cart(request):
    """
    This view returns the Shopping Cart Page
    """
    return render(request, 'cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the product to the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in cart:
        cart[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """ Adjust the quantity of the product to the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')
    else:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your Cart')
        
    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, item_id):
    """ Remove the item from the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})
    if item_id in cart:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your Cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
