from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.forms import UserChangeForm
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth import (
    authenticate,
    login,
    logout
)


# Create your views here.

def login_view(request):
    """This is the main Login Page view to log in a user"""
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)
    print(form.data)
    if form.is_valid():
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
    """ This is the main sign up view to register and authenticate a new user """
    form = RegisterForm(request.POST or None)
    print(request.POST)
    if form.is_valid():
        print("Valid")
        form.save()
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


class EditProfile(generic.UpdateView):

    """ This is edit profile class that is using the built-in UserChangeForm """

    form_class = UserChangeForm
    template_name = 'account/editprofile.html'
    success_url = reverse_lazy('home-url')

    def get_object(self):
        return self.request.user


def log_user(request):
    """ this is the Django view to logout a user and will called when the logout option from dropdown will be
    selected """

    logout(request)
    return redirect(reverse('login-url'))
