from django.shortcuts import render, redirect, Http404
from .forms import LoginForm, RegisterForm
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse
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


class EditProfile(UpdateView):

    """ This is edit profile class that is using the built-in UserChangeForm """

    template_name = 'account/user_form.html'
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(pk=pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get(pk=self.request.user.pk)
        except queryset.model.DoesNotExist:
            print("object not found")
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_success_url(self):
        return reverse('home-url')


def logout_user(request):
    """ this is the Django view to logout a user and will called when the logout option from dropdown will be
    selected """

    logout(request)
    return redirect(reverse('login-url'))
