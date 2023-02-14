from django.contrib import admin
from .models import Order, ProductInOrder, ProductInCart

class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    fields=['order', 'product', 'count']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)
    inlines = [ProductInOrderInline]

@admin.register(ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.get_fields()]

@admin.register(ProductInCart)
class ProductInCartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'product', 'count', 'price_per_item', 'total_price')
    list_display_links = ('session_key',)