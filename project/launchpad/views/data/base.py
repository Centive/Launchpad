import time
from math import floor

from django.http import JsonResponse


def standard_response(result=None):
    if result:
        return JsonResponse({
            'timestamp': floor(time.time()),
            'data': result,
        })
    else:
        return JsonResponse({
            'timestamp': floor(time.time()),
        })
