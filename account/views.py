from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model

from account.forms import UserForm

User = get_user_model()


def login(request):
    next_url = request.POST.get('next')
    print(next_url)

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if remember_me:
                    request.session.set_expiry(0)
                    request.session.modified = True
                    auth_login(request, user)

                auth_login(request, user)
                messages.success(request, f'{user.name if user.name else user.email}, welcome to Project Manager')
                return HttpResponseRedirect(next_url if next_url else '/')

            else:
                messages.error(request, 'Invalid credentials')
                return redirect('/login/')

    return render(request, 'account/login.html')


def signup(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        print(name, email, password1, password2)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('/signup/')

        if name and email and password1 and password2:
            User.objects.create_user(name=name, email=email, password=password1)

            return redirect('/login/')
        else:
            messages.error(request, 'Please fill all fields')
            return redirect('/signup/')

    return render(request, 'account/signup.html')


@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'account/login.html')


@login_required
def user_profile(request):
    try:
        user = User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        return render(request, 'account/profile.html', {'error': 'User does not exist'})

    if request.method == 'POST':
        update_user_form = UserForm(data=request.POST, instance=user)

        if update_user_form.is_valid():
            user = update_user_form.save()

            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']

            user.save()

            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating profile')
    else:
        update_user_form = UserForm(instance=user)

    request.user.refresh_from_db()

    return render(request, 'account/profile.html', {'update_user_form': update_user_form, 'user': user})


@login_required
def delete_user_avatar(request):
    request.user.avatar.delete()
    # request.user.save()

    return redirect('/profile/')
