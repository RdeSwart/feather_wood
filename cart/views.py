from django.shortcuts import render, redirect


def cart(request):
    """
    This view returns the Shopping Cart Page
    """
    return render(request, 'cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)
