import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from project.settings import env


@login_required
def verification(request):
    _user_id_external = request.user.id_external

    _sumsub_access_token_payload = {
        'userId': _user_id_external,
        'key': env('SUMSUB_KEY'),
    }

    _sumsub_request = requests.post(
        '/'.join([env('SUMSUB_HOST'), 'resources/accessTokens']),
        params=_sumsub_access_token_payload
    )

    _sumsub_response = _sumsub_request.json()

    return render(request, 'launchpad/verification.html', {
        'sumsub': {
            'host': env('SUMSUB_HOST'),
            'token': _sumsub_response['token'],
        }
    })
