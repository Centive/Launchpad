import random
from secrets import token_urlsafe

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from launchpad.forms.buy_forms import BuyForm
from launchpad.models import UserEligibilityRegistry, TokenOrders
from launchpad.services.pyCoinPayments import CryptoPayments
from project.settings import env


@login_required
def payment(request, order_id):
    _user_id_external = request.user.id_external

    _token_order = TokenOrders.objects.token_orders(
        customer_external_id=_user_id_external,
        token_order_external_id=order_id,
    )

    return render(request, 'launchpad/payment.html', {'token_order': _token_order[0]})
