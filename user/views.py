from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import LoginForm, RegistrationForm, ContactForm, UpdateUserForm
from .helpers import user_logged_in


# Create your views here.
def login(request):
    # remove sessions
    session_keys = (
        'user_logged_in',
        'user_id',
        'user_first_name',
        'user_last_name',
        'user_username',
        'user_email'
    )
    for sess_key in session_keys:
        if sess_key in request.session:
            del request.session[sess_key]

    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, "login.html", context)


def register(request):
    form = RegistrationForm()
    context = {
        'form': form 
    }
    return render(request, "register.html", context)


def contact(request):
    if user_logged_in(request.session): 
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, "contact.html", context)
    else:
        raise PermissionDenied


def profile(request):
    if user_logged_in(request.session): 
        form = UpdateUserForm()
        user_data = {
            'first_name': request.session['user_first_name'],
            'last_name': request.session['user_last_name'],
            'username': request.session['user_username'],
            'email': request.session['user_email'],
        }
        context = {
            'form' : form,
            'user_data' : user_data
        }
        return render(request, "profile.html", context)
    else:
        raise PermissionDenied