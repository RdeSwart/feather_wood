from django.shortcuts import render, redirect
from products.models import Product, WishlistItem
from django.contrib import messages


def index(request):
    """
    This view returns the Home Page rendering products on sale.
    """
    products_on_sale = Product.objects.filter(discount__gt=0)
    products_on_sale = [
        product for product in products_on_sale if product.sale_price < product.rrp_price
    ]

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'home/index.html', {
        'products': products_on_sale,
        'wishlist_items': wishlist_items,
    })


def about(request):
    """
    This view returns the About Page
    """
    return render(request, 'about.html', {})


def contact(request):
    """
    This view returns the Contact Us Page
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        messages.success(request, 'Thank you! Your enquiry has been sent.')
        return redirect('contact')

    return render(request, 'contact.html')
