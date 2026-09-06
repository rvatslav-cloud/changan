from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('app/<int:app_id>/', views.app_detail, name='app_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category'),
    path('free/', views.free_apps, name='free'),
    path('new/', views.new, name='new'),
    path('top/', views.top_paid, name='top'),
    path('nocategory/', views.no_category, name='no_category'),
    path('free/<int:category_id>/', views.free_in_category, name='free_in_category'),
    path('cheap/', views.cheap_apps, name='cheap'),
]