from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponse

from .models import App, Review, Category
# Create your views here.

def index(request):
    apps = App.objects.order_by('-created_at').all()
    featured = App.objects.order_by('-price').first()
    categories = Category.objects.all()
    return render(request, 'main/index.html',{
        'apps' : apps,
        'featured' : featured,
        'categories' : categories,
    })


def about(request):
    return render(request, 'main/about.html')

def reviews(request):
    all_reviews = Review.objects.order_by('-created_at').all()
    return render(request, 'main/reviews.html',{
        'reviews' : all_reviews,
    })

def app_detail(request,app_id):
    app = get_object_or_404(App, id = app_id)
    return render(request, 'main/app_detail.html', {'app': app})

def category_detail(request,category_id):
    category = get_object_or_404(Category, id =category_id)
    apps = App.objects.filter(category=category)
    return render(request, 'main/category.html', {
        'category' : category,
        'apps' : apps,
    })

def free_apps(request):
    apps = App.objects.filter(price=0).order_by('-created_at')
    return render(request, 'main/free.html',{'apps' : apps,})