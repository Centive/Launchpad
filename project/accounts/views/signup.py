from datetime import timedelta

from anymail.message import AnymailMessage
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.forms.signup_forms import SignupPrelimForm, SignupFinishSetupForm
from accounts.models import UserProfile
from accounts.services.exceptions import ServiceError


def signup_prelim(request):
    if request.method == 'POST':
        _signup_form = SignupPrelimForm(request.POST)

        if _signup_form.is_valid():
            _email = _signup_form.cleaned_data.get('email')

            _user = get_user_model()

            if _user.objects.user_exists(_email):
                _signup_form.add_error(None, mark_safe('This email you entered is already registered with us. Do you want to <a href="' + reverse('accounts:login') + '">login</a> instead?'))
                return render(request, 'accounts/signup_prelim.html', {'signup_form': _signup_form})

            else:
                _timedSigner = TimestampSigner()
                _signed_email = _timedSigner.sign(_email)

                _message = AnymailMessage(
                    to=[_email],
                    tags=['Onboarding']
                )
                _message.template_id = '4865e7c4-3b5a-498d-8487-c7a3ea593085'
                _message.merge_global_data = {
                    'signed_email': _signed_email,
                }
                _message.metadata = {'signed-email': _signed_email}
                _message.track_clicks = True

                _message.send()

                return redirect('accounts:signup-prelim-success')

        else:
            return render(request, 'accounts/signup_prelim.html', {'signup_form': _signup_form})

    else:
        _signup_form = SignupPrelimForm()
        return render(request, 'accounts/signup_prelim.html', {'signup_form': _signup_form})


def signup_prelim_success(request):
    return render(request, 'accounts/signup_prelim_success.html')


def signup_finish_setup(request, **kwargs):
    if 'signed_email' in kwargs:
        _signed_email = kwargs['signed_email']
        _user = get_user_model()

        if request.method == 'POST':
            _signup_form = SignupFinishSetupForm(request.POST, initial={'signed_email': _signed_email})

            if _signup_form.is_valid():
                _signed_email = _signup_form.cleaned_data.get('signed_email')
                try:
                    _timedSigner = TimestampSigner()
                    _email = _timedSigner.unsign(_signed_email)
                except (BadSignature, SignatureExpired):
                    return redirect('launchpad:home')

                if _user.objects.user_exists(_email):
                    # TODO: Logout and redirect to login
                    return redirect('launchpad:home')
                else:
                    _password = _signup_form.cleaned_data.get('password')
                    _user_model = get_user_model()

                    try:
                        with transaction.atomic():
                            _user = _user_model.objects.create_user(_email, _password)
                            _user.save()
                            _user_profile = UserProfile(user=_user)
                            _user_profile.save()

                    except (IntegrityError, ServiceError):
                        # TODO: Notify us of error
                        _signup_form.add_error(None, mark_safe('Oops! Something went wrong. Please try again later'))
                        return render(request, 'accounts/signup_finish_setup.html', {'signup_form': _signup_form})

                    # TODO: Send welcome email
                    _auth_user = auth.authenticate(request, username=_email, password=_password)

                    if _auth_user is not None:
                        auth.login(request, _auth_user)
                        return redirect('launchpad:home')
                    else:
                        auth.logout(request)
                        messages.success(request, '''Your account has been created!<br>
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

                return render(request, 'accounts/signup_finish_setup.html', {'signup_email': _email,
                                                                             'signup_form': _signup_form})

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

            if _user.objects.user_exists(_email):
                auth.logout(request)
                messages.info(request, 'You already hold a verified account with us. Please login.')
                return redirect('accounts:login')

            _signup_form = SignupFinishSetupForm(initial={'signed_email': _signed_email})

            return render(request, 'accounts/signup_finish_setup.html', {'signup_email': _email,
                                                                         'signup_form': _signup_form})

    else:
        return redirect('accounts:logout')
