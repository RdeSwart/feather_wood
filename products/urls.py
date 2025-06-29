from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<product_id>', views.product_detail, name='product_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist,
         name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist,
         name='remove_from_wishlist'),
    path('submit_review/<int:product_id>/', views.submit_review,
         name='submit_review'),
    path('edit_review/<int:review_id>/', views.edit_review,
         name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review,
         name='delete_review'),
]
