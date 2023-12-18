from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.http import FileResponse
from pathlib import Path

from camanagement.models import Camera
from common.camera_filter import camera_exists

# Create your views here.
@camera_exists
def get_list_of_records(request, cam_uuid):
    archive_path = settings.RECORD_FOLDER / str(cam_uuid)
    archive_files = list(map(lambda x: str(x).split('\\')[-1] ,list(archive_path.iterdir())))
    return render(request, 'record/archive_list.html', {
        'archive_list': archive_files,
        'uuid': cam_uuid
    })


@camera_exists
def download_record(request, cam_uuid, filename):
    return FileResponse(open(settings.RECORD_FOLDER / str(cam_uuid) / filename, 'rb'), as_attachment=True)