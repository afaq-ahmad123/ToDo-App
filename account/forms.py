from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = User.objects.filter(username=username).first()
            if user is None:
                raise forms.ValidationError('The user doesn\'t exist')
            # user = authenticate(username=username, password=password)
            print("Clean")
            print(user.is_active, user.check_password(password))

            if not user.is_active:
                raise forms.ValidationError("User Not activated")
            if not user.check_password(password):
                raise forms.ValidationError("Password Incorrect")


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(label='First Name', max_length=30, required=False)
    last_name = forms.CharField(label='Last Name', max_length=30, required=False)
    email = forms.EmailField(label='Email', max_length=254, required=True,
                             widget=forms.EmailInput(attrs={
                                            'placeholder': 'Enter valid Email address',
                                            'unique': True,
                             }))
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean(self, *args, **kwargs):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        if username and password:
            user = User.objects.get(email=email)
            if user:
                raise forms.ValidationError("User email already exists")

            user = authenticate([username, password])
            if user:
                raise forms.ValidationError('The user already exist')


class EditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']

