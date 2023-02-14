from django import forms
from .models import Order

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_address']
    # name = forms.CharField(label='name', max_length=100)
    # phone = forms.IntegerField(label='phone')
    # adress = forms.CharField(label='adress', max_length=255)