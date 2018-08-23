import datetime

import requests
from requests import RequestException

from launchpad.services.exceptions import ServiceError
from project import settings


class SaltEdgeService:
    @staticmethod
    def create_token(customer_secret=None, **kwargs):
        _url = 'https://www.saltedge.com/api/v4/tokens/create'

        try:
            if customer_secret is not None:
                _headers = {
                    'App-id': settings.SALT_EDGE['APP_ID'],
                    'Secret': settings.SALT_EDGE['SECRET'],
                    'Customer-secret': customer_secret,
                }

                _today_date = datetime.date.today().strftime('%Y-%m-%d')
                _tomorrow_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

                _data = {
                    'data': {
                        'include_fake_providers': True,
                        'show_consent_confirmation': False,
                        'javascript_callback_type': 'post_message',
                        'lost_connection_notify': True,
                        'allowed_countries': [kwargs['country_code']],
                        'provider_code': kwargs['provider_code'],
                        'fetch_scopes': [
                            'accounts',
                            # 'holder_info',
                            'transactions'
                        ],
                        'daily_refresh': True,
                        'from_date': _today_date,
                        'to_date': _tomorrow_date,
                    }
                }

                _r = requests.post(_url, headers=_headers, json=_data)
                _response = _r.json()

                if 'data' in _response:
                    _connect_data = {
                        'token': _response['data']['token'],
                        'expires_at': _response['data']['expires_at'],
                        'connect_url': _response['data']['connect_url'],
                    }

                    return _connect_data

                else:
                    raise RequestException
            else:
                raise ServiceError

        except (RequestException, ServiceError, KeyError):
            raise ServiceError

    @staticmethod
    def get_login(customer_secret=None, login_secret=None):
        _url = 'https://www.saltedge.com/api/v4/login'

        try:
            if customer_secret is not None and login_secret is not None:
                _headers = {
                    'App-id': settings.SALT_EDGE['APP_ID'],
                    'Secret': settings.SALT_EDGE['SECRET'],
                    'Customer-secret': customer_secret,
                    'Login-secret': login_secret,
                }

                _r = requests.get(_url, headers=_headers)
                _response = _r.json()

                if 'data' in _response:
                    _login_data = {
                        'id': _response['data']['id'],
                        'secret': _response['data']['secret'],
                        'status': _response['data']['status'],
                        'data': _response['data'],
                        'provider_code': _response['data']['provider_code'],
                    }

                    return _login_data

                else:
                    raise RequestException
            else:
                raise ServiceError

        except (RequestException, ServiceError, KeyError):
            raise ServiceError

    @staticmethod
    def get_accounts(customer_secret=None, login_secret=None):
        _url = 'https://www.saltedge.com/api/v4/accounts'

        try:
            if customer_secret is not None and login_secret is not None:
                _headers = {
                    'App-id': settings.SALT_EDGE['APP_ID'],
                    'Secret': settings.SALT_EDGE['SECRET'],
                    'Customer-secret': customer_secret,
                    'Login-secret': login_secret,
                }

                _r = requests.get(_url, headers=_headers)
                _response = _r.json()

                if 'data' in _response:
                    _accounts_data = []

                    for account in _response['data']:
                        _accounts_data.append({
                            'id': account['id'],
                            'name': account['name'],
                            'nature': account['nature'],
                            'currency_code': account['currency_code'],
                            'data': account,
                        })

                    return _accounts_data

                else:
                    raise RequestException
            else:
                raise ServiceError

        except (RequestException, ServiceError, KeyError):
            raise ServiceError
