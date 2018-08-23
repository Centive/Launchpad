import random
from secrets import token_urlsafe

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from launchpad.forms.buy_forms import BuyForm
from launchpad.models import UserEligibilityRegistry, TokenOrders
from launchpad.services.pyCoinPayments import CryptoPayments
from project.settings import env


@login_required
def buy(request):
    _user_id_external = request.user.id_external
    _user_email = request.user.email
    _user_eligibility_latest = UserEligibilityRegistry.objects.last_consent(external_id=_user_id_external)
    _token_cost_usd = 0.1

    if len(_user_eligibility_latest) == 0:
        return redirect('launchpad:eligibility')

    if request.method == 'POST':
        _buy_form = BuyForm(request.POST)

        if _buy_form.is_valid():
            _usd_value = _buy_form.cleaned_data.get('usd_value')
            _payment_currency = _buy_form.cleaned_data.get('payment_currency')

            _token_value = int(_usd_value) / _token_cost_usd
            _token_order_external_id = token_urlsafe(32)

            _cp_client = CryptoPayments(
                env('COINPAYMENTS_API_KEY'),
                env('COINPAYMENTS_API_SECRET'),
                env('COINPAYMENTS_IPN_URL'),
            )

            _token_order = TokenOrders(
                token_order_external_id=_token_order_external_id,
                customer_external_id=_user_id_external,
                usd_value=_usd_value,
                token_value=_token_value,
                payment_currency=_payment_currency,
            )

            _token_order.save()
            _token_order_id = _token_order.token_order_id

            _item_name = 'Centive Tokens (XTV)'
            _item_number = str(random.randint(10, 100)) + str(_token_order_id) + str(random.randint(10, 100))

            _cp_transaction = _cp_client.createTransaction({
                'amount': _usd_value,
                'currency1': 'USD',
                'currency2': _payment_currency,
                'buyer_email': _user_email,
                'item_name': _item_name,
                'item_number': _item_number,
            })

            _token_order.payment_currency_value = _cp_transaction.amount
            _token_order.payment_address = _cp_transaction.address
            _token_order.txn_id = _cp_transaction.txn_id
            _token_order.confirms_needed = _cp_transaction.confirms_needed
            _token_order.timeout = _cp_transaction.timeout
            _token_order.status_url = _cp_transaction.status_url
            _token_order.qrcode_url = _cp_transaction.qrcode_url

            _token_order.save()

            return redirect('launchpad:payment', order_id=_token_order_external_id)

        else:
            return render(request, 'launchpad/buy.html', {'buy_form': _buy_form})

    else:
        _buy_form = BuyForm()
        return render(request, 'launchpad/buy.html', {'buy_form': _buy_form})
