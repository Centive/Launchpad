from datetime import timedelta

from anymail.message import AnymailMessage
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.forms.password_reset_forms import PasswordResetPrelimForm, PasswordResetForm
from accounts.services.exceptions import ServiceError


def password_reset_prelim(request):
    if request.method == 'POST':
        _password_reset_prelim_form = PasswordResetPrelimForm(request.POST)

        if _password_reset_prelim_form.is_valid():
            _email = _password_reset_prelim_form.cleaned_data.get('email')

            _user = get_user_model()

            if _user.objects.user_exists(_email):
                _timedSigner = TimestampSigner()
                _signed_email = _timedSigner.sign(_email)

                _message = AnymailMessage(
                    to=[_email],
                    tags=['Account']
                )
                _message.template_id = 'a4753e4f-f898-4a97-8ca1-a52ef8cc7aeb'
                _message.merge_global_data = {
                    'signed_email': _signed_email,
                }
                _message.metadata = {'signed-email': _signed_email}
                _message.track_clicks = True

                _message.send()

                return redirect('accounts:password-reset-prelim-success')

            else:
                _password_reset_prelim_form.add_error(None,
                                                      mark_safe('This email is not registered with us. Do you want to <a href="' +
                                                                reverse('accounts:signup-prelim') +
                                                                '">signup</a> instead?'))
                return render(request, 'accounts/password_reset_prelim.html', {
                    'password_reset_prelim_form': _password_reset_prelim_form,
                })

        else:
            return render(request, 'accounts/password_reset_prelim.html', {
                'password_reset_prelim_form': _password_reset_prelim_form,
            })

    else:
        auth.logout(request)
        _password_reset_prelim_form = PasswordResetPrelimForm()
        return render(request, 'accounts/password_reset_prelim.html', {
            'password_reset_prelim_form': _password_reset_prelim_form,
        })


def password_reset_prelim_success(request):
    return render(request, 'accounts/password_reset_prelim_success.html')


def password_reset(request, **kwargs):
    if 'signed_email' in kwargs:
        _signed_email = kwargs['signed_email']
        _user = get_user_model()

        if request.method == 'POST':
            _password_reset_form = PasswordResetForm(request.POST, initial={'signed_email': _signed_email})

            if _password_reset_form.is_valid():
                _signed_email = _password_reset_form.cleaned_data.get('signed_email')
                try:
                    _timedSigner = TimestampSigner()
                    _email = _timedSigner.unsign(_signed_email)
                except (BadSignature, SignatureExpired):
                    return redirect('launchpad:home')

                if not _user.objects.user_exists(_email):
                    auth.logout(request)
                    return redirect('launchpad:login')
                else:
                    _password = _password_reset_form.cleaned_data.get('password')
                    _user_model = get_user_model()

                    _user_data = _user_model.objects.get_user_by_email(email=_email)
                    _user_data.set_password(_password)
                    _user_data.save()

                    _auth_user = auth.authenticate(request, username=_email, password=_password)

                    if _auth_user is not None:
                        auth.login(request, _auth_user)
                        return redirect('launchpad:home')
                    else:
                        auth.logout(request)
                        messages.success(request, '''Your password has been changed!<br>
                        Please login now to access your dashboard.''')
                        return redirect('accounts:login')

            else:
                try:
                    _timedSigner = TimestampSigner()
                    _email = _timedSigner.unsign(_signed_email, max_age=timedelta(days=2))

                except SignatureExpired:
                    auth.logout(request)
                    messages.error(request, '''Sorry, the verification link has expired.<br>
                    Please create a new account or login using an existing account.''')
                    return redirect('accounts:login')

                except BadSignature:
                    auth.logout(request)
                    messages.error(request, 'Sorry, it seems you followed through an invalid verification link.')
                    return redirect('accounts:login')

                return render(request, 'accounts/password_reset.html', {
                    'user_email': _email,
                    'password_reset_form': _password_reset_form,
                })

        else:
            try:
                _timedSigner = TimestampSigner()
                _email = _timedSigner.unsign(_signed_email, max_age=timedelta(days=2))

            except SignatureExpired:
                auth.logout(request)
                messages.error(request, '''Sorry, the password reset link has expired.<br>
                Please login or request a password reset again.''')
                return redirect('accounts:login')

            except BadSignature:
                auth.logout(request)
                messages.error(request, 'Sorry, it seems you followed through an invalid password reset link.')
                return redirect('accounts:login')

            if not _user.objects.user_exists(_email):
                auth.logout(request)
                messages.info(request, 'Sorry, we could not find your account in our system.')
                return redirect('accounts:login')

            _password_reset_form = PasswordResetForm(initial={'signed_email': _signed_email})

            return render(request, 'accounts/password_reset.html', {
                'user_email': _email,
                'password_reset_form': _password_reset_form,
            })

    else:
        return redirect('accounts:logout')
