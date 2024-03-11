from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
import os

from common.camera_filter import camera_exists

# Create your views here.
@camera_exists
def get_list_of_records(request, cam_uuid):
    archive_path = settings.RECORD_FOLDER / str(cam_uuid)
    archive_files = list(map(lambda x: str(x).split(os.sep)[-1] ,list(archive_path.iterdir())))
    return render(request, 'record/archive_list.html', {
        'archive_list': sorted(archive_files)[::-1],
        'uuid': cam_uuid
    })


@camera_exists
def download_record(request, cam_uuid, filename):
    return FileResponse(open(settings.RECORD_FOLDER / str(cam_uuid) / filename, 'rb'), as_attachment=True)
