from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Brand, WishlistItem
from django.contrib.auth.decorators import login_required


def all_products(request):
    """
    This view returns a list of all products, including
    a search and sort feature
    """

    products = Product.objects.all()
    query = None
    categories = None
    brands = None
    sort = None
    direction = None
    sortkey = 'lower_name'
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

        if sortkey == 'price_asc':
            sortkey = 'rrp_price'
        elif sortkey == 'price_desc':
            sortkey = '-rrp_price'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'brand' in request.GET:
            brand_names = request.GET['brand'].split(',')
            products = products.filter(brand__name__in=brand_names)
            brands = Brand.objects.filter(name__in=brand_names)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Oops! You need to type something to search for it!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_brands': brands,
        'current_sorting': current_sorting,
        
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    This view returns individual product details in full
    """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """
    This view returns wishlist items
    """

    product = get_object_or_404(Product, pk=product_id)
    redirect_url = request.POST.get('redirect_url', '/')

    wishlist_item, created = WishlistItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(request, f"{product.name} added to your wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")

    return redirect(redirect_url)


@login_required
def remove_from_wishlist(request, product_id):
    """
    Removes a product from the user's wishlist.
    """
    product = get_object_or_404(Product, pk=product_id)
    wishlist_item = WishlistItem.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f"{product.name} removed from your wishlist.")
    else:
        messages.info(request, f"{product.name} was not in your wishlist.")

    redirect_url = request.POST.get('redirect_url', '/profile/')
    return redirect(redirect_url)
