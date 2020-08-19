from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.urls import reverse
from django.contrib.auth import (
    authenticate,
    login,
    logout
)


# Create your views here.

def login_view(request):
    next = request.GET.get('next')
    # print(request.POST)
    form = LoginForm(request.POST or None)
    print(form.data)
    if form.is_valid():
        print("Valid")
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request=request, user=user)
            print("Logged In")

        if next:
            return redirect(next)
        else:
            return redirect(reverse('home-url'))

    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)


def signup_view(request):
    form = RegisterForm(request.POST or None)
    # return redirect(reverse('home-url'))
    print(request.POST)
    if form.is_valid():
        print("Valid")
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        print(user)
        login(request=request, user=user)
        return redirect(reverse('home-url'))

    context = {
        'form': form
    }
    return render(request, 'account/signup.html', context)


def edit_profile(request):
    return redirect(reverse('login-url'))


def log_user(request):
    logout(request)
    return redirect(reverse('login-url'))
