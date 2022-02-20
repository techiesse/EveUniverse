from functools import wraps
from django.views.decorators.csrf import csrf_exempt


def apiRequest(view):
    @csrf_exempt
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        return response

    return wrapper
