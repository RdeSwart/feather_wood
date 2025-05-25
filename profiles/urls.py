from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('wishlist/', views.user_wishlist_view, name='user_wishlist'),
]
