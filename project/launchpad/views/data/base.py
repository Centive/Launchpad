import time
from math import floor

from django.http import JsonResponse


def standard_response(result):
    return JsonResponse({
        'timestamp': floor(time.time()),
        'data': result,
    })
