from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter
def stars(value):
    full = int(value)
    return '★' * full + '☆' * (5 - full)


@register.filter
def reviews_count(value):
    value = int(value)
    if value % 10 ==1 and value % 100 != 11:
        return f'{value} отзыв'
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        return f'{value} отзыва'
    else:
        return f'{value} отзывов'


@register.filter
def apps_word(value):
    value = int(value)
    if value % 10 == 1 and value % 100 != 11:
        return f'{value} приложение'
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        return f'{value} приложения'
    else:
        return f'{value} приложений'


@register.filter
def categories_word(value):
    value = int(value)
    if value % 10 == 1 and value % 100 != 11:
        return f'{value} категория'
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        return f'{value} категории'
    else:
        return f'{value} категорий'


@register.simple_tag
def sale_percent(price, old_price):
    if not old_price:
        return ''
    percent = round(100 - price * 100 / old_price)
    return f'-{percent}%'

@register.simple_tag
def is_new(app):
    return app.created_at >= timezone.now() - timedelta(days=7)