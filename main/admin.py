from django.contrib import admin
from .models import Category, App, Review

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'downloads', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'downloads']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['username', 'app', 'stars', 'recommended', 'created_at']
    list_filter = ['stars', 'recommended', 'app']
    search_fields = ['username', 'comment']
    list_editable = ['stars', 'recommended']