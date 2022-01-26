
def apiRequest(view):
    def wrapper(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    return wrapper


