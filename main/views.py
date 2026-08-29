from django.shortcuts import render
from pyexpat import features

from .models import App, Review
# Create your views here.

def index(request):
    apps = App.objects.order_by('-created_at').all()
    featured = App.objects.order_by('-price').first()
    return render(request, 'main/index.html',{
        'apps' : apps,
        'featured' : featured,
    })


def about(request):
    return render(request, 'main/about.html')

def reviews(request):
    all_reviews = Review.objects.order_by('-created_at').all()
    return render(request, 'main/reviews.html',{
        'reviews' : all_reviews,
    })