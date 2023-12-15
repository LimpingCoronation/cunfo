from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.http import FileResponse
from django.urls import reverse
from camanagement.models import Camera

# Create your views here.

def get_hls_playlist(request, cam_uuid):
    cam = Camera.objects.filter(uuid=cam_uuid)
    if cam.exists():
        return FileResponse(open(settings.HLS_FOLDER / str(cam_uuid) / 'stream.m3u8', 'rb'))
    else:
        return HttpResponseRedirect(reverse('index'))
    

def get_hls_video(request, cam_uuid, filename):
    cam = Camera.objects.filter(uuid=cam_uuid)
    if cam.exists():
        return FileResponse(open(settings.HLS_FOLDER / str(cam_uuid) / filename, 'rb'), as_attachment=True)
    else:
        return HttpResponseRedirect(reverse('index'))
    

def get_hls_videoplayer(request, cam_uuid):
    return render(request, 'hls/stream.html', context={'uuid': cam_uuid, 'domain': settings.DOMAIN_NAME})