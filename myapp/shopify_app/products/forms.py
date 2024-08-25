# products/forms.py

from django import forms

class ProductForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)

class VariantForm(forms.Form):
    sku = forms.CharField()
    price = forms.DecimalField()
    image_url = forms.URLField()
