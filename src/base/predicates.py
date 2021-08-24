

def raises(exc, f, *args, **kwargs):
    try:
        f(*args, **kwargs)
        return False
    except exc:
        return True
