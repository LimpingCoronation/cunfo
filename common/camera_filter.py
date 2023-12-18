from django.shortcuts import HttpResponse
from functools import wraps

from camanagement.models import Camera


def camera_exists(func):
    @wraps(func)
    def wrapper(request, cam_uuid, *args, **kwargs):
        cam = Camera.objects.filter(uuid=cam_uuid)
        if cam.exists():
            return func(request, cam_uuid, *args, **kwargs)
        else:
            return HttpResponse('Camera not found...')
    return wrapper