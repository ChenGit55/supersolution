from django import forms
from .models import Sale, SaleItem
from apps.products.models import Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ()

class SaleItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())    
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price']
