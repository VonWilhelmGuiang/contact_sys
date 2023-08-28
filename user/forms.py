from django.core.exceptions import ValidationError
from django import forms
from .models import Account, Contact


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'id': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password'}))


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username'}))
    email = forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={'id': 'email'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'first_name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'last_name'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'id': 'password'}))
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'id': 'confirm_password'}))

    # verify if email already taken
    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered", code='409')
        else:
            return email


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'first_name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'last_name'}))
    phone = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'id': 'phone'}))
    company = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'company'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'id': 'email'}))

    #verify email address
    def clean_email(self):
        email = self.cleaned_data["email"]
        if Contact.objects.filter(email=email).exists():
            raise ValidationError("Email is already used by a contact", code='409')
        else:
            return email

