from django.conf import settings
import subprocess
from os import mkdir
from camanagement.models import RTSPRecording
from camanagement.models import RTSPRecording


def rtsp_record(record: RTSPRecording):
    folder = settings.RECORD_FOLDER / str(record.camera.uuid)

    if not folder.exists():
        mkdir(str(folder))

    ffmpeg_record = subprocess.Popen(
        f"""ffmpeg -i {record.camera.rtsp_url} -c copy -reset_timestamps 1 -map 0 -f segment -segment_time {int(record.duration)*60} -segment_format mp4 -segment_atclocktime 1 -strftime 1 {folder}/%Y_%m_%dT%H_%M_%S.mp4""".split(' '), 
        shell=False, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT
    )
    return ffmpeg_record.pid