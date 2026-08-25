from django.db import models


# Create your models here.

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
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    downloads = models.IntegerField(default=0, verbose_name='Количество скачиваний')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Приложения'
        verbose_name_plural = 'Приложения'


# 🔥 НОВАЯ МОДЕЛЬ Review
class Review(models.Model):
    app = models.ForeignKey(
        App,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Приложение'
    )
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    stars = models.IntegerField(
        default=5,
        choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')],
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