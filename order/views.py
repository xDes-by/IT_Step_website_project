from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import ProductInCart, Order, ProductInOrder, Product
from allauth.socialaccount.models import SocialAccount
from .forms import OrderForm


@csrf_exempt
def add_to_cart(request):
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get('pid')
    return_dict = {'products': []}
    if data.get('del'):
        item = get_object_or_404(ProductInCart, session_key=session_key, product_id=product_id)
        if item.count > 1:
            item.count -= 1
            item.save()
        else:
            item.delete()
    elif data.get('remove'):
        item = get_object_or_404(ProductInCart, session_key=session_key, product_id=product_id)
        item.delete()
    else:
        product = get_object_or_404(Product, id=product_id)
        if product.count > 0:
            item, created = ProductInCart.objects.get_or_create(
                session_key=session_key, product_id=product_id, defaults={'count': 1}
            )
            if not created:
                if product.count > item.count:
                    item.count += 1
                    item.save()
                    if product.count == item.count:
                        return_dict['can_buy'] = 'false'
                else:
                    return_dict['can_buy'] = 'false'
        else:
            return_dict['can_buy'] = 'false'

    products_in_cart = ProductInCart.objects.filter(session_key=session_key)
    product_count = sum(item.count for item in products_in_cart)

    for item in products_in_cart:
        product_dict = {
            'name': item.product.name,
            'total_price': item.total_price,
            'count': item.count,
        }
        return_dict['products'].append(product_dict)

    return_dict['product_count'] = product_count
    return JsonResponse(return_dict)


def order(request):
    form = OrderForm()
    social_account = SocialAccount.objects.get(user_id=request.user.id)
    session_key = request.session.session_key
    products_in_cart = ProductInCart.objects.filter(session_key=session_key)
    return render(request, 'order/order_list.html', locals())


def create_order(request):
    form = OrderForm(request.POST or None)
    session_key = request.session.session_key
    products_in_cart = ProductInCart.objects.filter(session_key=session_key)
    if request.method == "POST" and form.is_valid():
        data = request.POST
        customer_name = data['customer_name']
        customer_phone = data['customer_phone']
        customer_address = data['customer_address']
        user = SocialAccount.objects.get(user_id = request.user.id)
        order = Order.objects.create(user=user,
                                    customer_name = customer_name,
                                    customer_phone = customer_phone,
                                    customer_address = customer_address)
        for i in products_in_cart.values():
            ProductInOrder.objects.create(product_id=i['product_id'],
                                        count = i['count'],
                                        price_per_item=i['price_per_item'],
                                        total_price = i['total_price'],
                                        order=order)        
            products_in_cart.delete()     
            product_count_in_base = Product.objects.get(id=i['product_id'])   
            product_count_in_base.count = product_count_in_base.count - i['count']
            product_count_in_base.orders = product_count_in_base.orders + i['count']
            product_count_in_base.save(force_update = True)                                        
        return HttpResponseRedirect('/')
    else:
        form = OrderForm()
    return HttpResponseRedirect('/order/')
