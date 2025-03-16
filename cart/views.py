from django.shortcuts import render


def cart(request):
    """
    This view returns the Shopping Cart Page
    """
    return render(request, 'cart/cart.html')
