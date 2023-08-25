from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm

# Create your views here.
def login(request):
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