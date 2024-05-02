from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

from .models import User


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user:
                auth_login(request, user)

                return redirect('/')

    return render(request, 'account/login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if name and email and password1 and password2:
            user = User.objects.create_user(name=name, email=email, password=password1)

            return redirect('/login/')

    return render(request, 'account/signup.html')