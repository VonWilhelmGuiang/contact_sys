from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import LoginForm, RegistrationForm, ContactForm
from .helpers import user_logged_in


# Create your views here.
def login(request):
    # remove sessions
    session_keys = ('user_logged_in', 'user_id', 'user_first_name', 'user_last_name')
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
    form = ContactForm()
    context = {
        'form': form
    }
    if user_logged_in(request.session): 
        return render(request, "contact.html", context)
    else:
        raise PermissionDenied
