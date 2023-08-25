from django.core.exceptions import ValidationError
from django import forms
from .models import Account

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'id':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'password'}))



class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username'}))
    email = forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={'id': 'email'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'first_name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'last_name'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'id': 'password'}))
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'id': 'password'}))

    # verify if email already taken
    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered",code='409')
        else:
            return email