from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from launchpad.models import TermsPolicyRepo, UserTermsRegistry, TokenOrders


@login_required
def home(request):
    _user_id_external = request.user.id_external

    _terms_repo_latest = TermsPolicyRepo.objects.latest_term(term_type='terms-conditions')
    _user_term_latest = UserTermsRegistry.objects.last_consent(external_id=_user_id_external,
                                                               term_type='terms-conditions')

    if len(_user_term_latest) == 0 or _user_term_latest[0].term.term_id != _terms_repo_latest[0].term_id:
        return redirect('launchpad:terms')

    else:
        _pending_orders = TokenOrders.objects.token_orders(customer_external_id=_user_id_external).pending()
        return render(request, 'launchpad/home.html', {'pending_orders': _pending_orders})
