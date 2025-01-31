from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from config import settings


def signup(request):
    form =UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)
    context = {'form': form }
    return render(request, 'registration/signup.html', context)

def login(request):
    form = AuthenticationForm(request,request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(settings.LOGIN_REDIRECT_URL)

    context = {'form': form}
    return render(request, 'registration/login.html', context)



def logout(request):
    django_logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
