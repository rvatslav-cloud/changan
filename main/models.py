from decimal import Decimal,ROUND_HALF_UP


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

def validate_non_negative_price(value):
    if value < 0:
        raise ValidationError('Цена не может быть отрицательной')

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        validators=[validate_non_negative_price],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ImageField(upload_to='icons/', blank=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True,related_name='apps')
    favorited_by =models.ManyToManyField(User, related_name='favorite_apps', blank=True, verbose_name='В Избранном у',)
    rating_avg = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0,
        editable=False,
        verbose_name= 'Средняя оценка',
    )
    rating_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name= 'Число оценок',
    )

    downloads = models.IntegerField(default=0, verbose_name='Количество скачиваний')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:app_detail', kwargs = {'app_id' : self.pk})

    def price_label(self):
        if self.price == 0:
            return 'Бесплатно'
        return f'{self.price} $'

    def similar_by_price(self):
        return App.objects.filter(
            price__gte= self.price -10,
            price__lte= self.price +10,
        ).exclude(pk=self.pk)[:3]

    @classmethod
    def discount_paid(cls, persent):
        if type(persent) is not int or not 1 <= persent <=90:
            raise ValueError('Скидка должна быть целым числом от 1 до 90.')
        factor = (Decimal(100) - Decimal(persent)) / Decimal(100)
        paid = list(cls.objects.filter(price__gt=0))
        for app in paid:
            app.price = (app.price * factor).quantize(
                Decimal('0.01'),
                rounding=ROUND_HALF_UP,
            )
        return cls.objects.bulk_update(paid, ['price'])

    class Meta:
        verbose_name = 'Приложения'
        verbose_name_plural = 'Приложения'



class Review(models.Model):
    app = models.ForeignKey(
        App,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Приложение',

    )
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    stars = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MinValueValidator(1, message='Оценка должна быть от 1 до 5.'),
            MaxValueValidator(5, message='Оценка должна быть от 1 до 5.'),
        ],
        verbose_name='Оценка'
    )
    recommended = models.BooleanField(default=True, verbose_name='Рекомендует')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.username} → {self.app.name}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']