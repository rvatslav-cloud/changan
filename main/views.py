from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from .models import App, Review, Category
# Create your views here.

SORTS = {
    'new' : '-created_at',
    'name' : 'name',
    'price' : 'price',
    'expensive' : '-price',


}

def index(request):
    q = request.GET.get('q', '')
    sort = request.GET.get('sort', 'new')

    if q:
        apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else:
        apps = App.objects.all()

    apps = apps.order_by(SORTS.get(sort, '-created_at'))
    featured = App.objects.order_by('-price').first()
    categories = Category.objects.all()

    paginator = Paginator(apps,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/index.html',{
        'q' : q,
        'sort': sort,
        'page_obj' : page_obj,
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
    similar_by_price = App.objects.filter(
        price__gte=app.price - 30,
        price__lte=app.price + 30,
    ).exclude(id=app.id)[:3]
    return render(request, 'main/app_detail.html', {
        'app': app,
        'similar_by_price': similar_by_price,
    })

def category_detail(request,category_id):
    category = get_object_or_404(Category, id =category_id)
    q = request.GET.get('q', '')
    apps = App.objects.filter(category=category)
    if q:
        apps = apps.filter(Q(name__icontains=q) | Q(description__icontains=q)).order_by('name')
    else:
        apps = apps.order_by('-created_at')

    paginator = Paginator(apps,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    most_expensive = apps.order_by('-price').first()
    return render(request, 'main/category.html', {
        'category' : category,
        'page_obj' : page_obj,
        'most_expensive': most_expensive,
        'q' : q,
    })

def free_apps(request):
    apps = App.objects.filter(price=0).order_by('-created_at')
    return render(request, 'main/free.html',{'apps' : apps,})

def new(request):
    apps =App.objects.order_by('-created_at').all()

    paginator = Paginator(apps,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/new.html',{'page_obj' : page_obj})

def top_paid(request):
    apps = App.objects.filter(price__gt=0).order_by('-price')[:10]
    return render(request,'main/top.html',{'apps' : apps})


def no_category(request):
    apps = App.objects.filter(category=None)
    return render(request,'main/no_category.html',{'apps' : apps})


def free_in_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    apps = App.objects.filter(category=category, price=0)
    return render(request, 'main/free_in_category.html', {
        'category': category,
        'apps': apps,
    })


def cheap_apps(request):
    apps = App.objects.filter(price__lt = 100,price__gt = 0).order_by('price')
    return render(request,'main/cheap.html',{'apps' : apps})