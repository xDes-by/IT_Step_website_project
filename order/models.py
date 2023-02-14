from django.db import models
from django.db.models.signals import post_save
from products.models import Product
from allauth.socialaccount.models import SocialAccount

class Order(models.Model):
    user = models.ForeignKey(SocialAccount, blank=True, on_delete=models.CASCADE, default=None)
    customer_name = models.CharField(max_length=64, verbose_name='Покупатель', default=None)
    customer_phone = models.IntegerField(verbose_name='Телефон', default=None)
    customer_address = models.CharField(max_length=128, verbose_name='Адрес', default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма')#price*count

    def __str__(self):
        return 'Заказ № %s' % self.id

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE, default=None, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, verbose_name='Продукт')
    count = models.IntegerField(default=1, verbose_name='Количество')
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма')#price*count

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price
        self.total_price=self.product.price * self.count
        super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save(sender, instance, created, **kwargs):
    all_products_in_order = ProductInOrder.objects.filter(order=instance.order)
    for item in all_products_in_order:
        instance.order.total_price += item.total_price or 0
    instance.order.save()

post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInCart(models.Model):
    session_key = models.CharField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, verbose_name='Продукт')
    count = models.IntegerField(default=1, verbose_name='Количество')
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма')#price*count

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price
        self.total_price=self.product.price * self.count
        super(ProductInCart, self).save(*args, **kwargs)    






  