from django.views.decorators.csrf import csrf_protect
from .models import Account
from django.http import JsonResponse
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.hashers import make_password,check_password


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
                if(check_password(form.cleaned_data['password'],user['password'])):
                    request.session['user_id'] = user[id]
                    return JsonResponse({'success':True}, status=200)
                else:
                    return JsonResponse({ 'success':False, 'message': 'Incorrect password' }, status=403)    
            else:
                return JsonResponse({ 'success':False, 'message': 'User does not exist' }, status=404)
        else:
            return JsonResponse({'message': 'Bad Request'},status=400)
    else:
        return JsonResponse({'message': 'Invalid Request'},status=400)


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
                    password = make_password(form.cleaned_data['password'])
                )
                if insert:
                    return JsonResponse({'message': 'User Created'}, status=201)
                else:
                    return JsonResponse({'message': 'An error has occured'}, status=400)
            else:
                return JsonResponse({'message':'Password do not match'}, status= 403)
        else:
            if form.errors.as_json():
                return JsonResponse({'message': form.errors.as_json()}, status=400)
            else:
                return JsonResponse({'message': 'Invalid Request'},status=400)