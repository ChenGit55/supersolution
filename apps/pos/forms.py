from django import forms
from .models import Sale, SaleItem
from apps.products.models import Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["date"]

        widgets = {
            "date": forms.DateInput(attrs={'type': 'date'}),
        }

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price']
