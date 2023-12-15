from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout

from .forms import UserLoginForm, UserRegistrationForm


def sign_in(request):
    users = User.objects.all()
    if not users.exists():
        return HttpResponseRedirect(reverse('users:reg'))

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        context = {
            'form': UserLoginForm(),
        }
        return render(request, 'users/login.html', context=context)


def sign_up(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('users:login'))
        else:
            context = {
                'form': UserRegistrationForm(),
            }
            return render(request, 'users/reg.html', context=context)
    else:
        context = {
            'form': UserRegistrationForm(),
        }
        return render(request, 'users/reg.html', context=context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))