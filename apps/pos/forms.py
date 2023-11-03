from django import forms
from .models import SaleItem

class DatePickerWidget(forms.DateInput):
    input_type = 'text'

class DateForm(forms.Form):
    date = forms.DateField(widget=DatePickerWidget(attrs={'id': 'datepicker'}),required=False)

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price']
