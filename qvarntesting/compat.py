import six


def str_type(unicode):
    if six.PY2:
        return unicode.encode('utf-8')
    else:
        return unicode


def start_response(func):
    # Compatibility wrapper in order to make status and headers have correct
    # types for both py3 and py2 with unicode_literals enabled.
    def wrapper(status, headers):
        func(str_type(status), [(str_type(k), str_type(v)) for k, v in headers])
    return wrapper
