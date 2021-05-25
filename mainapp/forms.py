from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes import fields

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type'
        )


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User {username} not found.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Password is incorrect')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email']

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Confirm password'
        self.fields['phone'].label = 'Phone number'
        self.fields['first_name'].label = 'Name'
        self.fields['last_name'].label = 'Surname'
        self.fields['address'].label = 'Address'
        self.fields['email'].label = 'Email'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This email is already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Username {username} is already registered')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords should match')
        return self.cleaned_data