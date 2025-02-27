from django.shortcuts import render


def index(request):
    """
    This view returns the Home Page
    """
    return render(request, 'home/index.html')
