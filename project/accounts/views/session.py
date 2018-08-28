from django.conf import settings
from django.contrib import auth
from django.shortcuts import render, redirect
from django.urls import NoReverseMatch

from accounts.forms.session_forms import SessionLoginForm


def login_view(request):
    _next = request.GET.get('next', default=False)

    if request.method == 'POST':
        _login_form = SessionLoginForm(request.POST)

        if _login_form.is_valid():
            _email = _login_form.cleaned_data.get('email')
            _password = _login_form.cleaned_data.get('password')

            _user = auth.authenticate(request, username=_email, password=_password)

            if _user is not None:
                auth.login(request, _user)
                try:
                    print('Redirecting')
                    return redirect(_next or settings.LOGIN_REDIRECT_URL)
                except NoReverseMatch:
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                _login_form.add_error(None, 'Please check the email or password you entered')
                return render(request, 'accounts/login.html', {'login_form': _login_form})

    else:
        if request.user.is_authenticated:
            try:
                return redirect(_next or settings.LOGIN_REDIRECT_URL)
            except NoReverseMatch:
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            _login_form = SessionLoginForm()
            return render(request, 'accounts/login.html', {'login_form': _login_form})


def logout_view(request):
    auth.logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
