from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from launchpad.forms.eligibility_forms import EligibilityConfirmationForm
from launchpad.models import UserEligibilityRegistry


@login_required
def eligibility(request):
    _user_id_external = request.user.id_external
    _user_eligibility_latest = UserEligibilityRegistry.objects.last_consent(external_id=_user_id_external)

    if len(_user_eligibility_latest) == 0:
        if request.method == 'POST':
            _eligibility_form = EligibilityConfirmationForm(request.POST)

            if _eligibility_form.is_valid():
                _user_eligibility = UserEligibilityRegistry(customer_external_id=_user_id_external)
                _user_eligibility.save()

                return redirect('launchpad:buy')
            else:
                _eligibility_form.add_error(None, mark_safe('Oops! Something went wrong. Please try again later.'))

                return render(request, 'launchpad/eligibility.html', {
                    'eligibility_form': _eligibility_form,
                })
        else:
            _eligibility_form = EligibilityConfirmationForm()

            return render(request, 'launchpad/eligibility.html', {
                'eligibility_form': _eligibility_form,
            })
    else:
        return redirect('launchpad:buy')
