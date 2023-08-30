from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.http import QueryDict
from .models import Account, Contact
from .forms import LoginForm, RegistrationForm, ContactForm, UpdateUserForm
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
                    request.session['user_username'] = user['username']
                    request.session['user_email'] = user['email']
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


def view_contacts(request):
    if (request.method == "GET") and (user_logged_in(request.session)):
        # limit = rows_per_page * page
        # offset = rows_per_page * (page-1)
        offset = (int(request.GET['start'])) 
        limit = (int(request.GET['length'])) + offset
        draw = (int(request.GET['draw'])) #cast to int to prevent attacks

        result = []
        # if search value is supplied
        if request.GET['search[value]']:
            result = (
                    Contact.objects.filter(account__exact=request.session['user_id']) & 
                    (
                        Contact.objects.filter(first_name__icontains=request.GET['search[value]']) | 
                        Contact.objects.filter(last_name__icontains=request.GET['search[value]']) | 
                        Contact.objects.filter(phone__icontains=request.GET['search[value]']) | 
                        Contact.objects.filter(company__icontains=request.GET['search[value]']) | 
                        Contact.objects.filter(email__icontains=request.GET['search[value]'])
                    )
                ).order_by('id')[offset:limit]
        else:
            result = Contact.objects.filter(account__exact=request.session['user_id']).order_by('id')[offset:limit]

        result_list = list(result.values())
        number_of_records = Contact.objects.filter(account__exact=request.session['user_id']).count()
        return JsonResponse({'data':result_list, 'draw': draw, "recordsTotal": number_of_records,"recordsFiltered": number_of_records}, status=200)
    else:
        raise PermissionDenied


@csrf_protect
def update_account(request):
    if (request.method == "POST") and (user_logged_in(request.session)):
        form = UpdateUserForm(request.POST,check_email_exist=True, check_user_id=request.session['user_id'])
        if form.is_valid():
            # validate password
            if form.cleaned_data['new_password'] and form.cleaned_data['confirm_password'] and form.cleaned_data['current_password']:
                if form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']:
                    update = Account.objects.filter(id__exact=request.session['user_id']).update(
                        username = form.cleaned_data['username'],
                        email = form.cleaned_data['email'],
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        password = make_password(form.cleaned_data['new_password'])
                    )
                    if update:
                        # update session 
                        request.session['user_first_name'] = form.cleaned_data['first_name']
                        request.session['user_last_name'] = form.cleaned_data['last_name']
                        request.session['user_username'] = form.cleaned_data['username']
                        request.session['user_email'] = form.cleaned_data['email']
                        return JsonResponse({'success': True, 'message': 'Account Updated'}, status=201)
                    else:
                        return JsonResponse({'message': 'An error has occured'}, status=400)
                else:
                    return JsonResponse({'message': 'New Password does not match to Confirm Password'}, status=403)
            else:
                update = Account.objects.filter(id__exact=request.session['user_id']).update(
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                )
                if update:
                    # update session 
                    request.session['user_first_name'] = form.cleaned_data['first_name']
                    request.session['user_last_name'] = form.cleaned_data['last_name']
                    request.session['user_username'] = form.cleaned_data['username']
                    request.session['user_email'] = form.cleaned_data['email']
                    return JsonResponse({'success': True, 'message': 'Account Updated'}, status=201)
                else:
                    return JsonResponse({'message': 'An error has occured'}, status=400)
        else:
            return JsonResponse({'message': form.errors.as_json()}, status=403)
    else:
        raise PermissionDenied
    