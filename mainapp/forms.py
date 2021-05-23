from django import forms
from django.contrib.contenttypes import fields
from django.db import models

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type'
        )