from django.contrib import auth
from django.shortcuts import redirect
from django.urls import reverse


def login_action(request):
    username = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect(reverse('launchpad:home'))
    else:
        return redirect(reverse('accounts:login'))
