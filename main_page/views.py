from django.shortcuts import render
from products.models import Product, ProductCategory
from datetime import datetime


def index(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    date = datetime.strftime(datetime.now(), '%d/%m/%Y')
    
    top = [products.filter(category=i).order_by('-orders')[:3] for i in categories]

    context = {
        "top": top,
        "categories": categories,
        "title": "Магазин техники",
        "date": date
    }

    return render(request, 'main_page/main.html', context)
