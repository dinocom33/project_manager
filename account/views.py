from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

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


@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'account/login.html')


@login_required
def user_profile(request):
    if request.method == 'GET':
        name = request.user.name
        email = request.user.email
        bio = request.user.bio

        return render(request, 'account/profile.html', {'name': name, 'email': email, 'bio': bio})
    else:
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        bio = request.POST.get('bio', '')

        if name or email or bio:
            user = request.user
            user.name = name
            user.email = email
            user.bio = bio
            user.save()

            return redirect('account:profile')

    return render(request, 'account/profile.html')
