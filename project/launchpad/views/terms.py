from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from launchpad.forms.terms_forms import TermsAcceptanceForm
from launchpad.models import TermsPolicyRepo, UserTermsRegistry


@login_required
def terms(request):
    _user_id_external = request.user.id_external
    _terms_repo_latest = TermsPolicyRepo.objects.latest_term(term_type='terms-conditions')
    _user_term_latest = UserTermsRegistry.objects.last_consent(external_id=_user_id_external,
                                                               term_type='terms-conditions')

    if len(_user_term_latest) == 0 or _user_term_latest[0].term.term_id != _terms_repo_latest[0].term_id:
        if request.method == 'POST':
            _terms_form = TermsAcceptanceForm(request.POST)

            if _terms_form.is_valid():
                _term_type = _terms_form.cleaned_data.get('term_type')
                _term_version = _terms_form.cleaned_data.get('term_version')

                _terms_repo_data = TermsPolicyRepo.objects.terms(term_type=_term_type, term_version=_term_version)

                if len(_terms_repo_data) > 0:
                    _user_term = UserTermsRegistry(customer_external_id=_user_id_external,
                                                   term=_terms_repo_data[0])
                    _user_term.save()

                    return redirect('launchpad:home')
                else:
                    _terms_form.add_error(None, mark_safe('Oops! Something went wrong. Please try again later.'))

                    return render(request, 'launchpad/terms.html', {
                        'terms_data': _terms_repo_latest[0],
                        'terms_form': _terms_form
                    })

            else:
                return render(request, 'launchpad/terms.html', {
                    'terms_data': _terms_repo_latest[0],
                    'terms_form': _terms_form
                })

        else:
            _terms_form = TermsAcceptanceForm(initial={
                'term_type': 'terms-conditions',
                'term_version': _terms_repo_latest[0].term_version
            })

            return render(request, 'launchpad/terms.html', {
                'terms_data': _terms_repo_latest[0],
                'terms_form': _terms_form,
            })
    else:
        return redirect('launchpad:home')
