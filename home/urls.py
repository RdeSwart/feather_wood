from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about.html', views.about, name='about'),
]
