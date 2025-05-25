from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Brand, WishlistItem, ProductReview
from .forms import ProductReviewForm
from django.contrib.auth.decorators import login_required
from checkout.models import OrderLineItem


def all_products(request):
    """
    This view returns a list of all products, with search, filter, and sorting.
    """
    products = Product.objects.all()
    query = None
    categories = None
    brands = None
    sort = None
    direction = None

    if request.GET:
        sort = request.GET.get('sort')
        direction = request.GET.get('direction')
        sortkey = sort

        if sort == 'name':
            sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower('name'))
        elif sort == 'price':
            sortkey = 'rrp_price'
        elif sort == 'rating':
            sortkey = 'rating'
        elif sort == 'category':
            sortkey = 'category__friendly_name'

        if direction == 'desc':
            sortkey = f'-{sortkey}'

        if sort:
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
                messages.error(
                    request,
                    "Oops! You need to type something to search for it!"
                )
                return redirect(reverse('products'))

            queries = (
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            products = products.filter(queries)

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    current_sorting = f'{sort}_{direction}' if sort and direction else 'None_None'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_brands': brands,
        'current_sorting': current_sorting,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    This view returns individual product details in full
    """

    product = get_object_or_404(Product, pk=product_id)

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'product': product,
        'wishlist_items': wishlist_items,
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
    wishlist_item = WishlistItem.objects.filter(user=request.user,
                                                product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request,
                         f"{product.name} removed from your wishlist.")
    else:
        messages.info(request, f"{product.name} was not in your wishlist.")

    redirect_url = request.POST.get('redirect_url', '/profile/')
    return redirect(redirect_url)


@login_required
def submit_review(request, product_id):
    """
    This view allows logged in Users to create a product review.
    """
    product = get_object_or_404(Product, id=product_id)

    has_purchased = OrderLineItem.objects.filter(
        order__user_profile=request.user.userprofile,
        product=product
    ).exists()

    if not has_purchased:
        messages.error(request, "You can only review products you've purchased.")
        return redirect('profile')

    if ProductReview.objects.filter(user=request.user, product=product).exists():
        messages.info(request, "You've already submitted a "
                        "review for this product.")
        return redirect('profile')

    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Thank you! Your review "
                            "has been submitted.")
            return redirect('profile')
        else:
            messages.error(request, "There was an error with your review.")
    else:
        form = ProductReviewForm()

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/submit_review.html', context)
