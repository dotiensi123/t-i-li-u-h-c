from django import forms

class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập số lượng'
        })
    )
