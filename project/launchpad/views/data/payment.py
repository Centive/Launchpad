import json
from secrets import token_urlsafe

from anymail.message import AnymailMessage
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
        _send_success_email = False
        _send_cancel_email = False

        if 'merchant' not in request.POST or request.POST.get('merchant') != env('COINPAYMENTS_MERCHANT_ID'):
            _param_errors.append('merchant')

        if not _param_errors:
            if request.POST.get('ipn_type') == 'api':
                _txn_id = request.POST.get('txn_id')
                _status = int(request.POST.get('status'))
                _status_text = request.POST.get('status_text')
                _email = request.POST.get('email')

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
                                _send_success_email = True

                            _order.payment_received = True
                            _order.tokens_credited = True

                        elif _status == -1:
                            _send_cancel_email = True

                        _order.save()

                        if _send_success_email:
                            _message = AnymailMessage(
                                to=[_email],
                                tags=['Orders']
                            )
                            _message.template_id = 'a33525c2-8c99-4f8e-b7cd-b943e874c318'
                            _message.merge_global_data = {
                                'token_value': ' '.join([str("{:,.2f}".format(float(_order.token_value))), 'XTV']),
                            }
                            _message.metadata = {'payment-address': _order.payment_address}
                            _message.track_clicks = True

                            _message.send()

                        elif _send_cancel_email:
                            _message = AnymailMessage(
                                to=[_email],
                                tags=['Orders']
                            )
                            _message.template_id = 'f39a80c3-a381-4a15-822b-32fb08debbe4'
                            _message.merge_global_data = {
                                'token_value': ' '.join([str("{:,.2f}".format(float(_order.token_value))), 'XTV']),
                                'payment_currency_value': ' '.join([str(_order.payment_currency_value), _order.payment_currency]),
                                'payment_address': _order.payment_address,
                            }
                            _message.metadata = {'payment-address': _order.payment_address}
                            _message.track_clicks = True

                            _message.send()

                        return standard_response()

                except IntegrityError:
                    # TODO: Notify us of error
                    return standard_response()

        else:
            return HttpResponse('Missing required parameters: %s' % ', '.join(_param_errors), status=400)
    else:
        return HttpResponse('Method Not Allowed', status=405)
