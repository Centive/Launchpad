import time
from math import floor

from django.http import JsonResponse


def standard_response(result=None):
    return JsonResponse({
        'timestamp': floor(time.time()),
        'data': result,
    })
