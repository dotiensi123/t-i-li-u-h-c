from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . models import UserProfile

def home(request):
     return redirect('books:book_list')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('books:book_list')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('books:book_list')

def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            login(request, new_user)
            return redirect('users:login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'form': user_form})

@login_required(login_url='users:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('books:book_list')
    else:
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': user_form})

@login_required(login_url='users:login')
@user_passes_test(lambda user: user.is_superuser)
def all_user(request):
    users = UserProfile.objects.all().select_related('user')
    return render(request, 'all_user.html', {'users': users})
