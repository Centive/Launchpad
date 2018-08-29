import json
from secrets import token_urlsafe

from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from launchpad.models import TokenOrders, TokenTransactions
from launchpad.views.data.base import standard_response
from project.settings import env


@csrf_exempt
def update(request):
    if request.method == 'POST':
        _param_errors = []

        if 'merchant' not in request.POST or request.POST.get('merchant') != env('COINPAYMENTS_MERCHANT_ID'):
            _param_errors.append('merchant')

        if not _param_errors:
            if request.POST.get('ipn_type') == 'api':
                _txn_id = request.POST.get('txn_id')
                _status = int(request.POST.get('status'))
                _status_text = request.POST.get('status_text')

                try:
                    with transaction.atomic():
                        _order = TokenOrders.objects.order_from_txn(txn_id=_txn_id).get()
                        _order.payment_status = _status
                        _order.payment_status_text = _status_text

                        if _status >= 1:
                            if not _order.tokens_credited:
                                _transaction = TokenTransactions(
                                    token_transaction_external_id=token_urlsafe(32),
                                    customer_external_id=_order.customer_external_id,
                                    transaction_type='Deposit',
                                    token_value=_order.token_value,
                                )

                                _transaction.save()

                            _order.payment_received = True
                            _order.tokens_credited = True

                        _order.save()

                        return standard_response()

                except IntegrityError:
                    # TODO: Notify us of error
                    return standard_response()

        else:
            return HttpResponse('Missing required parameters: %s' % ', '.join(_param_errors), status=400)
    else:
        return HttpResponse('Method Not Allowed', status=405)
