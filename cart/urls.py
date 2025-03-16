from django.urls import path
from . import views

urlpatterns = [
    path('cart.html', views.view_cart, name='view_cart'),
]