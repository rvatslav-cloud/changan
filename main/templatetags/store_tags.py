from django import template

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
