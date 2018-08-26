from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from launchpad.models import TokenTransactions


@login_required
def transactions(request):
    _user_id_external = request.user.id_external

    _transactions = TokenTransactions.objects.token_transactions(customer_external_id=_user_id_external)
    return render(request, 'launchpad/transactions.html', {'transactions': _transactions})
