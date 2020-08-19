from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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

    # email1 = forms.CharField(label='Email', widget=forms.EmailInput)
    # email2 = forms.CharField(label='Confirm Email', widget=forms.EmailInput)
    # password = forms.CharField(label='password', widget=forms.PasswordInput)

    first_name = forms.CharField(label='First Name', max_length=30, required=False)
    last_name = forms.CharField(label='Last Name', max_length=30, required=False)
    email = forms.EmailField(label='Email', max_length=254, required=True,
                             widget=forms.EmailInput(attrs={
                                            'placeholder': 'Enter valid Email address',
                                            'unique': True,
                             }))
    username = forms.CharField(required=True)
    # pk = User.objects.count()
    # password1 = forms.CharField(required=True, widget=forms.PasswordInput)

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

    # def clean(self):
    #     email1 = self.cleaned_data['email1']
    #     email2 = self.cleaned_data['email2']
    #     if email1 != email2:
    #         raise forms.ValidationError('Emails don\'t match')
    #     if User.objects.filter(email=email1).exists():
    #         raise forms.ValidationError('User already exists')
    #
    #     return email1
