from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .backend import AuthBackend


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password doesn't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):

    # password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kwargs):
        super(UserAdminChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['task_count'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial.get('password')


class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        super(LoginForm, self).clean(*args, **kwargs)
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
            if not user.is_authenticated:
                raise forms.ValidationError("User Not authenticated")
            if not user.check_password(password):
                raise forms.ValidationError("Password Incorrect")


class RegisterForm(forms.ModelForm):#UserCreationForm

    first_name = forms.CharField(label='First Name', max_length=30, required=False)
    last_name = forms.CharField(label='Last Name', max_length=30, required=False)
    email = forms.EmailField(label='Email', max_length=254, required=True,
                             widget=forms.EmailInput(attrs={
                                            'placeholder': 'Enter valid Email address',
                                            'unique': True,
                             }))
    username = forms.CharField(required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        obj = User.objects.filter(username=username)
        if obj.exists():
            raise forms.ValidationError("Username Taken")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.authenticated = True
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password doesn't match")
        return password2

    def clean(self, *args, **kwargs):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        if username and password:
            user = User.objects.filter(email=email).first()
            if user:
                raise forms.ValidationError("User email already exists")
            auth = AuthBackend()
            user = auth.authenticate(username=username, password=password)
            if user:
                raise forms.ValidationError('The user already exist')


class EditForm(forms.ModelForm):#UserChangeForm
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        self.request = kwargs['instance']
        print(self.request.username)
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['task_count'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'task_count']

    def clean(self):
        username = self.cleaned_data.get('username')
        print(self.request.username)
        user = User.objects.filter(username=username).first()
        if user and user.username != self.request.username:
            self.cleaned_data['username'] = self.cleaned_data.get('username')
            raise forms.ValidationError("Username Already exists")

        super(EditForm, self).clean()
