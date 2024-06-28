from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='', widget=forms.Select(attrs={"class": "form-control text-center", "style":"max-width: 3rem; border-color: black;"}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())
    
