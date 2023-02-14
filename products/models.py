from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='Категория')
    image = models.ImageField(upload_to='images/product/', verbose_name='Фото')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'


class Product(models.Model):
    name = models.CharField(max_length=64, default=None, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="Категория")
    description = models.TextField(max_length=500, verbose_name="Описание")
    image = models.ImageField(upload_to='images/product/', verbose_name="Фото")
    count = models.IntegerField(verbose_name="Количество")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    memory = models.CharField(max_length=30, verbose_name="Оперативная память")
    cpu = models.CharField(max_length=30, verbose_name="ЦПУ")
    screen = models.CharField(max_length=30, verbose_name="Размер экрана")
    orders = models.IntegerField(verbose_name="Покупок", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

