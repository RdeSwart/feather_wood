from django.shortcuts import render
from products.models import Product, WishlistItem


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
    return render(request, 'contact.html', {})
