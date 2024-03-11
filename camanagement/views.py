from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from os import kill
import psutil

from common.ffmpeg_translation import create_ffmpeg_translation
from common.ffmpeg_recording import rtsp_record
from common.camera_filter import camera_exists
from common.utils import union_querysets
from .forms import CameraForm, HLSFormResolution, RecordForm
from .models import Camera, HLSTranslation, RTSPRecording
from .dto import ProcDTO

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
        form = HLSFormResolution(request.POST)
        if cam.exists() and form.is_valid():
            cam = cam.first()
            pid = create_ffmpeg_translation(
                camera=cam,
                bitrate=form.cleaned_data['bitrate'],
                quality=form.cleaned_data['quality'],
                resolution=form.cleaned_data['resolution'],
            )
            hls_translation = HLSTranslation.objects.create(
                pid=pid, 
                camera=cam,
                bitrate=form.cleaned_data['bitrate'],
                quality=form.cleaned_data['quality'],
                resolution=form.cleaned_data['resolution'],    
            )
            hls_translation.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'camanagement/launch_hls.html', context={'form': HLSFormResolution()})
    else:
        return render(request, 'camanagement/launch_hls.html', context={'form': HLSFormResolution()})
    

@login_required
def launch_record(request):
    if request.method == "POST":
        cam = Camera.objects.filter(name=request.POST['name'])
        form = RecordForm(request.POST)
        if cam.exists() and form.is_valid():
            cam = cam.first()
            print(form.cleaned_data['bitrate'])
            record_proc = rtsp_record(
                uuid=cam.uuid, 
                duration=form.cleaned_data['duration'], 
                rtsp_url=cam.rtsp_url, 
                days=form.cleaned_data['days'],
                bitrate=form.cleaned_data['bitrate'],
                quality=form.cleaned_data['quality'],
            )
            record = RTSPRecording.objects.create(
                pid=record_proc, 
                duration=form.cleaned_data['duration'], 
                days=form.cleaned_data['days'], 
                camera=cam, 
                bitrate=form.cleaned_data['bitrate'],
                quality=form.cleaned_data['quality'],
            )
            record.save()
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


@login_required
def processes_list(request):
    translations = union_querysets(HLSTranslation.objects.all(), RTSPRecording.objects.all())
    proc_list = [ProcDTO(pid=translation.pid, cam_name=translation.camera.name, type_=(1 if isinstance(translation, RTSPRecording) else 0)) for translation in translations]
    return render(request, 'camanagement/translation_list.html', context={
        'processes': proc_list 
    })


@login_required
def kill_proc(request, pid):
    try:
        translations = union_querysets(HLSTranslation.objects.all(), RTSPRecording.objects.all())
        for translation in translations:
            if translation.pid == pid:
                p = psutil.Process(pid)
                p.kill()
                translation.delete()
                return HttpResponseRedirect(reverse('camanagement:proc_list'))
        return HttpResponse('Cannot kill non-existent process')
    except Exception as e:
        print(e)
        return HttpResponse('Cannot kill non-existent process')

