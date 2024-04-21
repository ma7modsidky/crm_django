from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
# Create your views here.

def home(request):
    return render(request, 'website/home.html', {})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you have been logged in successfully')
                return redirect('home')
            else:
                messages.error(request, 'There was an error, please try again')
                return render(request, 'website/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'website/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')