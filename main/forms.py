from django import forms
from django.forms import ModelForm

from .models import Review, App


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['username', 'comment', 'stars', 'recommended']
        labels = {
            'username': 'Ваше имя',
            'comment' : 'Комментарий',
            'stars' : 'Оценка (1 - 5)',
            'recommended' : 'Рекомендую',
        }

    def clean_stars(self):
        stars = self.cleaned_data['stars']
        if stars < 1 or stars > 5:
            raise forms.ValidationError('Оценка должна быть от 1 до 5.')
        return stars

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'description', 'price','category', 'icon']
        labels = {
            'name' : 'Название',
            'description' : 'Оприсание',
            'price' : 'Цена',
            'category' : 'Категория',
            'icon' : 'Иконка',
        }
