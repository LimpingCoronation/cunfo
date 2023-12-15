from django.conf import settings
import ffmpeg
from datetime import datetime, timedelta
from time import time, sleep
from os import mkdir
from multiprocessing import Process
from camanagement.models import RTSPRecording
from record.models import Record
from camanagement.models import RTSPRecording


def rtsp_record(record: RTSPRecording):
    duration = int(record.duration)
    rtsp = record.camera.rtsp_url
    folder = settings.RECORD_FOLDER / str(record.camera.uuid)

    if not folder.exists():
        mkdir(str(folder))

    stream = ffmpeg.input(rtsp)

    while True:
        part = Record.objects.create(record=record, filename=f"{time()}",end=(datetime.now()+timedelta(minutes=duration)))
        part.save()
        name = f"{folder}/part-{part.filename}.avi"
        process = Process(target=stream.output(name).run_async, daemon=True)
        process.start()
        sleep(duration*60)
        process.terminate() 