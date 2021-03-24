from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def process_registration(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        request.session['userid'] = user.id
        return redirect(f'/success/{first_name}')

def process_login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    else:
        email = request.POST['email_login']
        password = request.POST['password_login']
        user = User.objects.get(email=email)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['userid'] = user.id
            return redirect(f'/success/{user.first_name}')

def success(request, first_name):
    context = {
        "first_name": first_name,
    }
    return render(request, 'success.html', context)
