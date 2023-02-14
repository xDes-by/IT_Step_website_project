from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import Product, ProductCategory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_photo', 'name', 'description', 'price', 'count', 'category', 'color', "screen", "memory", "cpu", "orders")
    list_display_links = ('name', 'get_photo')
    search_fields = ('name', 'description')
    list_filter = ('category', 'memory', 'color', 'screen', 'cpu')

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50"')
        else:
            return "Нет фото"

    get_photo.short_description = "Фото"


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('get_photo', 'name')
    list_display_links = ('name', 'get_photo')
    search_fields = ('name',)

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100"')
        else:
            return "Нет фото"

    get_photo.short_description = "Фото"



admin.site.site_title = "Админка магазина техники"
admin.site.site_header = "Админка магазина техники"
