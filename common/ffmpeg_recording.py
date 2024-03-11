from django.conf import settings
import subprocess
from os import mkdir
from multiprocessing import Process

from .file_cleaner import file_cleaner
from camanagement.models import RTSPRecording
from camanagement.models import RTSPRecording


def rtsp_record(uuid, duration, rtsp_url, days, bitrate, quality):
    folder = settings.RECORD_FOLDER / str(uuid)

    if not folder.exists():
        mkdir(str(folder))

    Process(target=file_cleaner, args=(folder, days)).start()

    ffmpeg_record = subprocess.Popen(
        f"""ffmpeg -i {rtsp_url} -c:v libx264 -b:v {bitrate}k -crf {quality} -map 0 -f segment -segment_time {int(duration)*60} -segment_format flv -segment_atclocktime 1 -strftime 1 {folder}/%Y_%m_%dT%H_%M_%S.flv""".split(' '), 
        shell=False, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL,
	    bufsize=0,
    )
    return ffmpeg_record.pid
