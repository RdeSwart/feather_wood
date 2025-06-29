from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from cart.contexts import cart_contents
from profiles.forms import UserProfileForm
from profiles.models import UserProfile

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'city': request.POST['city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    quantity = item_data if isinstance(item_data, int) else item_data.get('quantity', 0)
                    if quantity > 0:
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found."
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))
            order.update_total()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_no]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Looks like you have nothing in your cart'
                                    ' at the moment.')
            return redirect(reverse('products'))

    current_cart = cart_contents(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'city': profile.default_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            })
        except UserProfile.DoesNotExist:
            order_form = OrderForm()
    else:
        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing, did you'
                         'forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_no):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_no=order_no)

    profile = UserProfile.objects.get(user=request.user)
    order.user_profile = profile
    order.save()

    if save_info:
        profile_data = {
            'default_phone_number': order.phone_number,
            'default_street_address1': order.street_address1,
            'default_street_address2': order.street_address2,
            'default_city': order.city,
            'default_county': order.county,
            'default_country': order.country,
            'default_postcode': order.postcode,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_no}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)


@login_required
def order_history(request, order_no):
    """
    A view to display past order confirmation from the profile page
    """
    order = get_object_or_404(Order, order_no=order_no)

    messages.info(request, f'This is a past confirmation for order number {order_no}. '
                           f'A confirmation email was sent on the order date.')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }
    return render(request, template, context)
