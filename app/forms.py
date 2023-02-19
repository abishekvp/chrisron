from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class user_form(forms.Form):
    wallet_address = forms.CharField(max_length=50)
    timer = forms.CharField(max_length=25)
    claim = forms.IntegerField(max_value=50000)
    withdrawl = forms.IntegerField(max_value=None)
    password = forms.CharField(max_length=20)
