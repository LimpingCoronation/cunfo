from functools import wraps
from django.shortcuts import render
from django.conf import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip  = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ip_filter(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if get_client_ip(request) in settings.ALLOWED_IPS:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'camanagement/banned.html')
    return wrapper