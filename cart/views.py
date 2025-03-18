from django.shortcuts import render, redirect, reverse, HttpResponse


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

    if item_id in cart:
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """ Adjust the quantity of the product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if item_id in cart:
        cart[item_id] = quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, item_id):
    """ Remove the item from the shopping bag """
    cart = request.session.get('cart', {})
    if item_id in cart:
        cart.pop(item_id)
        request.session['cart'] = cart
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
