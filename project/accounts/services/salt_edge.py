import requests
from requests import RequestException

from accounts.services.exceptions import ServiceError
from project import settings


class SaltEdgeService:
    @staticmethod
    def create_customer(identifier):
        _url = 'https://www.saltedge.com/api/v4/customers'

        _headers = {
            'App-id': settings.SALT_EDGE['APP_ID'],
            'Secret': settings.SALT_EDGE['SECRET'],
        }

        _data = {
            'data': {
                'identifier': identifier,
            }
        }

        try:
            _r = requests.post(_url, headers=_headers, json=_data)
            _response = _r.json()

            if 'data' in _response:
                _customer = {
                    'se_customer_id': _response['data']['id'],
                    'customer_external_id': _response['data']['identifier'],
                    'se_customer_secret': _response['data']['secret'],
                }

                return _customer

            else:
                raise RequestException

        except RequestException:
            raise ServiceError
