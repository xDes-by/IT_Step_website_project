from django.contrib import admin
from django.urls import path, include
from main_page import views as mp
from products import views as pr
from order import views as order
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mp.index),
    path('order/', order.order),
    path('create_order/', order.create_order, name='create_order'),
    path('shop/', pr.ProductsView.as_view()),
    path('filter/', pr.FilterProductsView.as_view(), name='filter'),
    path('add_to_cart/', order.add_to_cart, name='add_to_cart'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)