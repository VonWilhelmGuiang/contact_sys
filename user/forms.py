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
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'first_name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'last_name'}))
    phone = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'phone'}))
    company = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'company'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'email'}))
    check_email_exist = False
    check_user_id = 0

    def __init__(self, *args, **kwargs):
        self.check_email_exist = kwargs.pop('check_email_exist',False)
        self.check_user_id = kwargs.pop('check_user_id',0)
        super(ContactForm, self).__init__(*args, **kwargs)


    #verify email address
    def clean_email(self):
        email = self.cleaned_data["email"]
        check_email_exist = self.check_email_exist
        check_user_id = self.check_user_id
        # for update
        if check_email_exist == True:
            # if email DID NOT CHANGED, continue
            if Contact.objects.filter(email=email, id=check_user_id).exists():
                return email
            #if email CHANGED, verify
            else:
                if Contact.objects.filter(email=email).exists():
                    raise ValidationError("Email is already used by a contact", code='409')
                else:
                    return email
        else:
            # check email if it already exist
            if Contact.objects.filter(email=email).exists():
                raise ValidationError("Email is already used by a contact", code='409')
            else:
                return email