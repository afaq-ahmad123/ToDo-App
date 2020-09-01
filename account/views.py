from django.shortcuts import render, redirect, Http404
from .forms import LoginForm, RegisterForm, EditForm
from django.views.generic import UpdateView
from account.models import User
from django.urls import reverse
from django.contrib import messages
from .backend import AuthBackend
from .decorators import login_required
from django.utils.decorators import method_decorator



# # Create your views here.
# class LoginView(FormView):
#     """login view"""
#
#     form_class = LoginForm
#     # success_url = reverse('home-url')
#     template_name = 'account/login.html'
#
#     def form_valid(self, form):
#         """ process user login"""
#         credentials = form.cleaned_data
#
#         user = authenticate(username=credentials['username'],
#                             password=credentials['password'])
#
#         if user is not None:
#             login(self.request, user)
#             return HttpResponseRedirect(reverse('home-url'))
#
#         else:
#             messages.add_message(self.request, messages.INFO, 'Wrong credentials')
#
#             return HttpResponseRedirect(reverse('login-url'))

def login_view(request):
    """This is the main Login Page view to log in a user"""

    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            auth = AuthBackend()
            user = auth.authenticate(username=username, password=password)
            if user:
                AuthBackend.login(request, user)
            next_url = request.POST.get('next')
            if next_url is not None:
                return redirect(reverse('home-url'))
                return redirect(next_url)
            else:
                return redirect(reverse('home-url'))

    context = {
        'form': form,
        'next': None,
    }
    if next_url is not None:
        context['next'] = next_url
    return render(request, 'account/login.html', context)


def signup_view(request):
    """ This is the main sign up view to register and authenticate a new user """
    form = RegisterForm(request.POST or None)
    print(request.POST)
    if form.is_valid():
        print("Valid")
        username = form.cleaned_data.get('username')
        form.save(commit=True)
        user = User.objects.filter(username=username).first()
        AuthBackend.login(request, user)
        return redirect(reverse('home-url'))

    context = {
        'form': form
    }
    return render(request, 'account/signup.html', context)


@method_decorator(login_required, name="dispatch")
class EditProfile(UpdateView):

    """ This is edit profile class that is using the built-in UserChangeForm """

    template_name = 'account/user_form.html'
    model = User
    form_class = EditForm
    # fields = ['username', 'first_name', 'last_name', 'email',]

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(id=pk)
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
    request = AuthBackend.logout(request)
    return redirect(reverse('login-url'))
