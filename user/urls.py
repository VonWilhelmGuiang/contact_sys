from django.urls import path
from . import views
from . import ajax


urlpatterns = [
    # view urls
    path('', views.login, name="login"),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name="contact"),
    path('profile/', views.profile, name="profile"),
    
    # ajax urls
    path('user/auth', ajax.authenticate_user, name="authenticate_user"),
    path('user/create', ajax.create_user, name="create_user"),
    path('contact/create', ajax.create_contact, name="create_contact"),
    path('contact/edit_contact/<int:contact_id>', ajax.edit_contact, name="edit_contact"),
    # path('contact/view_contacts/<int:page>/<int:rows_per_page>', ajax.view_contacts, name="view_contacts"),
    path('contact/view_contacts/', ajax.view_contacts, name="view_contacts"),
    path('account/update',ajax.update_account, name="account_update")
]
