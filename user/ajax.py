from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.http import QueryDict
from .models import Account, Contact
from .forms import LoginForm, RegistrationForm, ContactForm
from .helpers import user_logged_in


@csrf_protect
def authenticate_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        #validate form
        if form.is_valid():
            email = form.cleaned_data['email']
            user = Account.objects.filter(email__exact=email).values().first()
            #user exist
            if user:
                # check password
                if(check_password(form.cleaned_data['password'], user['password'])):
                    request.session['user_logged_in'] = True
                    request.session['user_id'] = user['id']
                    request.session['user_first_name'] = user['first_name']
                    request.session['user_last_name'] = user['last_name']
                    return JsonResponse({'success': True}, status=200)
                else:
                    return JsonResponse({ 'success': False, 'message': 'Incorrect password' }, status=403)    
            else:
                return JsonResponse({ 'success': False, 'message': 'User does not exist' }, status=404)
        else:
            return JsonResponse({'message': 'Bad Request'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid Request'}, status=400)


@csrf_protect
def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        # validate form
        if form.is_valid():
            # validate password
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                insert = Account.objects.create(
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    password = make_password(form.cleaned_data['password']),
                    active = True
                )
                if insert:
                    return JsonResponse({'success': True, 'message': 'User Created'}, status=201)
                else:
                    return JsonResponse({'message': 'An error has occured'}, status=400)
            else:
                return JsonResponse({'message': 'Password do not match'}, status= 403)
        else:
            if form.errors.as_json():
                return JsonResponse({'message': form.errors.as_json()}, status=400)
            else:
                return JsonResponse({'message': 'Invalid Request'}, status=400)


@csrf_protect
def create_contact(request):
    if (request.method == "POST") and (user_logged_in(request.session)):
        form = ContactForm(request.POST)

        #validate form
        if form.is_valid():
            user_account_id = Account.objects.filter(id__exact=request.session['user_id']).only('id').first()
            insert = Contact.objects.create(
                account = user_account_id,
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                phone = form.cleaned_data['phone'],
                company = form.cleaned_data['company'],
                email = form.cleaned_data['email']
            )
            if insert:
                return JsonResponse({'success': True, 'message': 'Contact Created'}, status=201)
            else:
                return JsonResponse({'message': 'An error has occured'}, status=400)
        else:
            return JsonResponse({'message': form.errors.as_json()}, status=400)
    else:
        raise PermissionDenied


@csrf_protect
def edit_contact(request, contact_id):
    if (request.method == "PUT") and (user_logged_in(request.session)):

        put = QueryDict(request.body)
        form = ContactForm(put,check_email_exist=True, check_user_id=contact_id)

        if form.is_valid():
            update = Contact.objects.filter(id__exact=contact_id).update(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                phone = form.cleaned_data['phone'],
                company = form.cleaned_data['company'],
                email = form.cleaned_data['email']
            )
            if update:
                return JsonResponse({'success': True, 'message': 'Contact Updated'}, status=201)
            else:
                return JsonResponse({'message': 'An error has occured'}, status=400)
        else:
            return JsonResponse({'message': form.errors.as_json()}, status=400)
    else:
        raise PermissionDenied


def view_contacts(request, page, rows_per_page):
    if (request.method == "GET") and (user_logged_in(request.session)):
        limit = rows_per_page * page
        offset = rows_per_page * (page-1)
        result = Contact.objects.filter(account__exact=request.session['user_id']).order_by('id')[offset:limit]
        result_list = list(result.values())
        return JsonResponse({'contacts':result_list}, status=200)
    else:
        raise PermissionDenied
