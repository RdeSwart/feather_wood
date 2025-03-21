from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Looks like you have nothing in your cart at the moment")
        return redirect(reverse('products'))
        
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QjKxEJgmT1h7J9HudI0QOGeGmob8M7Kz4KvyU7x30QjR1P0tf3dTjEYdEMFNsZ48WnLcpW0H47hAb2w2ZvDXAbG00WX4huLu2',
    }

    return render(request, template, context)
