from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        help_texts = {
            'comment': 'Можно использовать: [b]жирный[/b], [i]курсив[/i], [list][*]пункт[/list]',
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
            'description' : 'Описание',
            'price' : 'Цена',
            'category' : 'Категория',
            'icon' : 'Иконка',
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = 'Электронная почта')
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Введите пароль'
        self.fields['password2'].label = 'Повторите пароль'

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Аккаунт с такой почтой уже есть.')
        return email


class PurchaseFilterForm(forms.Form):
    date_from =forms.DateField(
        label='С',
        required=False,
        widget=forms.DateInput(attrs={'type':'date'}),
    )
    date_to = forms.DateField(
        label='По',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from is not None and date_to is not None and date_from > date_to:
            raise forms.ValidationError('Дата "С" не может быть позже даты "По"')
        return cleaned_data


class PriceFilterForm(forms.Form):
    price_min = forms.DecimalField(label='Цена от', required=False)
    price_max = forms.DecimalField(label='Цена до', required=False)
    sort = forms.ChoiceField(
        label='Порядок',
        required=False,
        choices=[
            ('', 'по умолчанию'),
            ('price', 'сначала дешёвые'),
            ('-price', 'сначала дорогие'),
        ],
    )

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')
        if price_min is not None and price_max is not None and price_min > price_max:
            raise forms.ValidationError('Цена «от» не может быть больше цены «до»')
        return cleaned_data