from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order
from products.models import WishlistItem


def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profiles.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True       
    }
 
    return render(request, template, context)


def order_history(request, order_no):
    """ Display the user's order history. """

    order = get_object_or_404(Order, order_no=order_no)

    messages.info(request, (
        f'This is a past confirmation for order number {order_no}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def user_wishlist_view(request):
    """ Display the user's wishlist items. """
    
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    # Instead of .get(), use .filter() to get all individual wishlist items
    wishlist_items = WishlistItem.objects.filter(user=request.user)

    form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'wishlist_items': wishlist_items,
    }

    return render(request, template, context)
