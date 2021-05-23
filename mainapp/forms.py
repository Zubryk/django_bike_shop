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