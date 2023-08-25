from django.urls import path
from . import views
from . import ajax

urlpatterns = [
    # view urls
    path('', views.login),
    path('register/', views.register),
    
    # ajax urls
    path('user/auth', ajax.authenticate_user, name="authenticate_user"),
    path('user/create', ajax.create_user, name="create_user"),
]
