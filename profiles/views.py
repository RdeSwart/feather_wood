from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import UserProfile
from .forms import UserProfileForm
from products.models import WishlistItem, Product, ProductReview
from products.forms import ProductReviewForm


@login_required
def profile(request):
    """ Display user's profile, orders, and reviewable products """

    user_profile = get_object_or_404(UserProfile, user=request.user)
    orders = user_profile.orders.all()
    wishlist_items = WishlistItem.objects.filter(user=request.user)

    if request.method == 'POST' and 'save_profile' in request.POST:
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
        else:
            messages.error(request, 'Failed to update profile. Please check the form.')
    else:
        form = UserProfileForm(instance=user_profile)

    purchased_products = Product.objects.filter(
        orderlineitem__order__user_profile=user_profile
    ).distinct()

    submitted_reviews = ProductReview.objects.filter(user=request.user)

    context = {
        'profile': user_profile,
        'form': form,
        'orders': orders,
        'wishlist_items': wishlist_items,
        'purchased_products': purchased_products,
        'submitted_reviews': submitted_reviews,
        'review_form': ProductReviewForm(),
    }

    return render(request, 'profiles/profiles.html', context)


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
