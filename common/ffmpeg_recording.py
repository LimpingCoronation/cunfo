from django.conf import settings
import subprocess
from os import mkdir
from multiprocessing import Process

from .file_cleaner import file_cleaner
from camanagement.models import RTSPRecording
from camanagement.models import RTSPRecording


def rtsp_record(record: RTSPRecording):
    folder = settings.RECORD_FOLDER / str(record.camera.uuid)

    if not folder.exists():
        mkdir(str(folder))

    Process(target=file_cleaner, args=(folder,)).start()

    ffmpeg_record = subprocess.Popen(
        f"""ffmpeg -i {record.camera.rtsp_url} -c:v libx264 -b:v 4M -crf 20 -map 0 -f segment -segment_time {int(record.duration)*60} -segment_format flv -segment_atclocktime 1 -strftime 1 {folder}/%Y_%m_%dT%H_%M_%S.flv""".split(' '), 
        shell=False, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT
    )
    return ffmpeg_record.pid