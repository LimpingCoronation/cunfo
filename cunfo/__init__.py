from pathlib import Path
from django.conf import settings
from os import mkdir, kill
import atexit
from os import kill
from common.utils import union_querysets


def kill_process(pid):
    try:
        kill(pid)
    except:
        pass


def startup():
    if not settings.HLS_FOLDER.exists():
        mkdir(settings.HLS_FOLDER)
    
    if not settings.RECORD_FOLDER.exists():
        mkdir(settings.RECORD_FOLDER)

def kill_process(pid):
    try:
        kill(pid)
    except:
        pass


def stopserver():
    from camanagement.models import HLSTranslation, RTSPRecording
    translations = union_querysets(HLSTranslation.objects.all(), RTSPRecording.objects.all())

    for translation in translations:
        kill_process(translation.pid)
        translation.delete()


atexit.register(stopserver)

startup()