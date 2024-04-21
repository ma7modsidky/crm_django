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
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'website/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'website/login.html', {'form': form})