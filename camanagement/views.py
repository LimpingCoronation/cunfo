from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from .forms import CameraForm, HLSForm, RecordForm
from .models import Camera, HLSTranslation, RTSPRecording

from common.ffmpeg_translation import create_ffmpeg_translation
from common.ffmpeg_recording import rtsp_record
from common.camera_filter import camera_exists

# Create your views here.
@login_required
def index(request):
    return render(request, "camanagement/index.html")


@login_required
def add_cam(request):
    if request.method == "POST":
        form = CameraForm(request.POST)
        if form.is_valid():
            cam = Camera.objects.create(
                name=request.POST['name'], 
                rtsp_url=request.POST['rtsp_url'], 
                uuid=uuid4())
            cam.save()
            return HttpResponseRedirect(reverse('camanagement:add_cam'))
        else:
            return render(request, 'camanagement/add_cam.html', context={'form': CameraForm()})
    else:
        context = {
            'form': CameraForm(),
            'btn_label': 'Add',
        }
        return render(request, 'camanagement/add_cam.html', context=context)
    

@login_required
def launch_hls(request):
    if request.method == "POST":
        cam = Camera.objects.filter(name=request.POST['name'])
        if cam.exists():
            cam = cam.first()
            pid = create_ffmpeg_translation(cam)
            hls_translation = HLSTranslation.objects.create(pid=pid, camera=cam)
            hls_translation.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'camanagement/launch_hls.html', context={'form': HLSForm()})
    else:
        return render(request, 'camanagement/launch_hls.html', context={'form': HLSForm()})
    

@login_required
def launch_record(request):
    if request.method == "POST":
        cam = Camera.objects.filter(name=request.POST['name'])
        form = RecordForm(request.POST)
        if cam.exists() and form.is_valid():
            cam = cam.first()
            record = RTSPRecording.objects.create(duration=request.POST['duration'], camera=cam)
            record.save()
            rtsp_record(record)
            return HttpResponseRedirect(reverse('index'))
        else:
           return render(request, 'camanagement/launch_record.html', context={'form': RecordForm()})
    else:
        return render(request, 'camanagement/launch_record.html', context={'form': RecordForm()})
    

@login_required
def camera_list(request):
    cameras = Camera.objects.all()
    return render(request, 'camanagement/cameras_list.html', context={'cameras': cameras})


@login_required
@camera_exists
def delete_camera(request, cam_uuid):
    camera = Camera.objects.get(uuid=cam_uuid)
    camera.delete()
    return HttpResponseRedirect(reverse('camanagement:cameras_list'))


@login_required
@camera_exists
def update_camera(request, cam_uuid):
    cam = Camera.objects.get(uuid=cam_uuid)
    if request.method == 'POST':
        form = CameraForm(request.POST)
        cam.name = form.data['name']
        cam.rtsp_url = form.data['rtsp_url']
        cam.save()
        return HttpResponseRedirect(reverse('camanagement:cameras_list'))
    else:
        return render(request, 'camanagement/add_cam.html', context={
            'form': CameraForm({'name': cam.name, 'rtsp_url': cam.rtsp_url}),
            'uuid': cam.uuid,
            'btn_label': 'Update',
        })
