from django.http import HttpResponse, JsonResponse
import json


def jsonSuccessResponse(data):
    content = {
        'data': data,
        'status': 'ok',
    }
    return JsonResponse(data = content)


def jsonFailureResponse(error):
    content = {
        'error': error,
        'status': 'fail',
    }
    return JsonResponse(data = content)
