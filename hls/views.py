from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.http import FileResponse
from django.urls import reverse

from camanagement.models import Camera
from common.camera_filter import camera_exists

# Create your views here.

@camera_exists
def get_hls_playlist(request, cam_uuid):
    return FileResponse(open(settings.HLS_FOLDER / str(cam_uuid) / 'stream.m3u8', 'rb'))
    

@camera_exists
def get_hls_video(request, cam_uuid, filename):
    return FileResponse(open(settings.HLS_FOLDER / str(cam_uuid) / filename, 'rb'), as_attachment=True)
    

@camera_exists
def get_hls_videoplayer(request, cam_uuid):
    return render(request, 'hls/stream.html', context={'uuid': cam_uuid, 'domain': settings.DOMAIN_NAME})