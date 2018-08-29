import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from launchpad.views.data.base import standard_response
from project.settings import env


@csrf_exempt
def update(request):
    if request.method == 'POST':
        _param_errors = []
        _params = {}

        # _request_body = json.loads(request.body.decode("utf-8"))

        _file_handle = open('/home/ubuntu/ipn.log', 'w+')
        _file_handle.write(str(request.POST))
        _file_handle.close()

        return HttpResponse('OK', status=200)

        # if 'merchant' not in _request_body or _request_body['merchant'] != env('COINPAYMENTS_MERCHANT_ID'):
        #     _param_errors.append('merchant')
        #
        # if 'ipn_type' in _request_body:
        #     if _request_body['ipn_type'] == 'deposit':
        #         _address = _request_body['address']
        #         _txn_id = _request_body['txn_id']
        #         _status = _request_body['status']
        #         _status_text = _request_body['status_text']
        #
        # if 'provider-code' in _request_body:
        #     _params['provider_code'] = _request_body['provider-code']
        # else:
        #     _param_errors.append('provider-code')
        #
        # if not _param_errors:
        #     # _se_customer = SaltEdgeCustomers.objects.customers(external_id=_user_id_external)[0]
        #     # _connect_data = SaltEdgeService.create_token(_se_customer.se_customer_secret, **_params)
        #
        #     return standard_response(_connect_data)
        # else:
        #     return HttpResponse('Missing required parameters: %s' % ', '.join(_param_errors), status=400)
    else:
        return HttpResponse('Method Not Allowed', status=405)
