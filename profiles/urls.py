from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_no>', views.order_history, name='order_history'),
    path('wishlist/', views.user_wishlist_view, name='user_wishlist'),
]
