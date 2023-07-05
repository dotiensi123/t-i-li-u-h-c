from django import forms

class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(max_length=50)