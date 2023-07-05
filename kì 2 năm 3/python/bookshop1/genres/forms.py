from django import forms
from .models import Genres

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = ('name',)
