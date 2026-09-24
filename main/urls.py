from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('about/', views.AboutView.as_view(), name='about'),

    path('reviews/', views.reviews, name='reviews'),
    path('app/<int:app_id>/review/', views.add_review, name='add_review'),


    path('app/<int:app_id>/', views.AppDetailView.as_view(), name='app_detail'),
    path('app/<int:app_id>/<str:app_name>/', views.app_detail_with_app_name,name='app_detail_with_app_name'),

    path('category/<int:category_id>/', views.category_detail, name='category'),

    path('free/', views.free_apps, name='free'),

    path('new/', views.new, name='new'),

    path('top/', views.top_paid, name='top'),

    path('nocategory/', views.no_category, name='no_category'),

    path('free/<int:category_id>/', views.free_in_category, name='free_in_category'),
    path('cheap/', views.cheap_apps, name='cheap'),

    path('api/app/<int:app_id>/', views.app_json, name='app_json'),

    path('free-apps/', views.apps_list, {'is_free': True}, name='free_apps'),
    path('paid-apps/', views.apps_list, {'is_free': False}, name='paid_apps'),

    path('add-app/', views.add_app,  name='add_app'),

]