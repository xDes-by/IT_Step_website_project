# Generated by Django 4.1.4 on 2023-02-14 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('socialaccount', '0004_openidnonce_openidstore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(default=None, max_length=64, verbose_name='Покупатель')),
                ('customer_phone', models.IntegerField(default=None, verbose_name='Телефон')),
                ('customer_address', models.CharField(default=None, max_length=128, verbose_name='Адрес')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='socialaccount.socialaccount')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='ProductInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='Количество')),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма')),
                ('order', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
            },
        ),
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=250)),
                ('count', models.IntegerField(default=1, verbose_name='Количество')),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]