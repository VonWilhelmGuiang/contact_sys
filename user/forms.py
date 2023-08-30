from django.core.exceptions import ValidationError
from django import forms
from .models import Account, Contact
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control'}))


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username', 'class': 'form-control'}))
    email = forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control'}))
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'id': 'confirm_password', 'class': 'form-control'}))


    # verify if email already taken
    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered", code='409')
        else:
            return email


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'first_name form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'last_name form-control'}))
    phone = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'phone form-control'}))
    company = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'company form-control'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'email form-control'}))
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


class UpdateUserForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username', 'class': 'form-control'}))
    email = forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'first_name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'last_name', 'class': 'form-control'}))
    current_password = forms.CharField(max_length=32, required=False,  widget=forms.PasswordInput(attrs={'id': 'current_password', 'class': 'form-control'}))
    new_password = forms.CharField(max_length=32, required=False, widget=forms.PasswordInput(attrs={'id': 'new_password', 'class': 'form-control'}))
    confirm_password = forms.CharField(max_length=32, required=False, widget=forms.PasswordInput(attrs={'id': 'confirm_password', 'class': 'form-control'}))
    check_email_exist = False
    check_user_id = 0


    def __init__(self, *args, **kwargs):
        self.check_email_exist = kwargs.pop('check_email_exist',False)
        self.check_user_id = kwargs.pop('check_user_id',0)
        super(UpdateUserForm, self).__init__(*args, **kwargs)
    

    #verify email address
    def clean_email(self):
        email = self.cleaned_data["email"]
        check_email_exist = self.check_email_exist
        check_user_id = self.check_user_id
        # for update
        if check_email_exist == True:
            # if email DID NOT CHANGED, continue
            if Account.objects.filter(email=email, id=check_user_id).exists():
                return email
            #if email CHANGED, verify
            else:
                if Account.objects.filter(email=email).exists():
                    raise ValidationError("Email is already used by another user", code='409')
                else:
                    return email
        else:
            # check email if it already exist
            if Account.objects.filter(email=email).exists():
                raise ValidationError("Email is already used by another user", code='409')
            else:
                return email


    # if password is filled : check if current password match
    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        check_user_id = self.check_user_id
        if current_password and current_password is not None: 
            user = Account.objects.filter(id__exact=check_user_id).values().first()
            # check if current password match
            if check_password(current_password,user['password']):
                return(self.cleaned_data['current_password'])
            else:
                raise ValidationError("Current password is incorrect", code='403')
        else:
            return(self.cleaned_data['current_password'])
