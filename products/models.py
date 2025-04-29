from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=300)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey('Brand', null=True, blank=True, on_delete=models.SET_NULL)
    details = models.CharField(max_length=250)
    description = models.TextField()
    rrp_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    @property
    def discounted_price(self):
        return round(self.rrp_price - self.discount, 2)
   
    @property
    def sale_price(self):
        return round(self.rrp_price - self.discount, 2)

    def __str__(self):
        return self.name
    
    def get_star_rating(self):
        # Ensure the rating is a number between 0 and 5
        score = self.rating if self.rating else 0
        score = min(max(score, 0), 5)

        full_stars = int(score)  # number of full stars
        half_star = 1 if score - full_stars >= 0.5 else 0  # half star
        empty_stars = 5 - full_stars - half_star  # empty stars

        # Construct the HTML string based on the stars
        star_rating_html = ""

        # Add full stars
        for _ in range(full_stars):
            star_rating_html += '<i class="bi bi-star-fill text-warning"></i>'

        # Add half star
        if half_star:
            star_rating_html += '<i class="bi bi-star-half text-warning"></i>'

        # Add empty stars
        for _ in range(empty_stars):
            star_rating_html += '<i class="bi bi-star text-warning"></i>'

        return star_rating_html


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=300)
    friendly_name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name
     
    def get_friendly_name(self):
        return self.friendly_name


class Brand(models.Model):
    name = models.CharField(max_length=300)
    friendly_name = models.CharField(max_length=300, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
   
    def get_friendly_name(self):
        return self.friendly_name
    

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
