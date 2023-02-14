from django.db.models import Q
from django.views.generic import ListView
from products.models import Product, ProductCategory

class Gets:
    def get_categoty(self):
        return ProductCategory.objects.all()

    def get_screens(self):
        return Product.objects.values_list('screen', flat=True).distinct()


class ProductsView(Gets, ListView):
    paginate_by = 8
    model = Product
    template_name ='shop_page/product_list.html'  # без этого идет на main_page/product_list (возможно потому что модель в другом приложении)
    

class FilterProductsView(Gets, ListView):
    template_name = 'shop_page/product_list.html' # без этого идет на main_page/product_list (возможно потому что модель в другом приложении)
    paginate_by = 8

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(category__in=self.request.GET.getlist("category")) |
            Q(screen__in=self.request.GET.getlist("screen"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        context["screen"] = ''.join([f"screen={x}&" for x in self.request.GET.getlist("screen")])
        return context