from django.shortcuts import render
from .models import Product


# Create your views here.
def all_products(request):
    """
    This view returns a list of all products, including
    a search and sort feature
    """

    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)