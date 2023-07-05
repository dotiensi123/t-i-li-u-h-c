from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'address', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, address=self.cleaned_data['address'], phone_number=self.cleaned_data['phone_number'])
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, required=True)
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'address', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile.address = self.cleaned_data['address']
            user.profile.phone_number = self.cleaned_data['phone_number']
            user.profile.save()
        return user
