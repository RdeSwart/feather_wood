from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import UserProfile
from .forms import UserProfileForm
from products.models import WishlistItem


def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist_items = WishlistItem.objects.filter(user=request.user)

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
        'wishlist_items': wishlist_items,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def user_wishlist_view(request):
    """ Display the user's wishlist items. """

    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    wishlist_items = WishlistItem.objects.filter(user=request.user)

    form = UserProfileForm(instance=profile)

    template = 'profiles/profiles.html'
    context = {
        'form': form,
        'orders': orders,
        'wishlist_items': wishlist_items,
    }

    return render(request, template, context)
