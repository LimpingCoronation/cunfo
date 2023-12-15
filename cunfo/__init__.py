from pathlib import Path
from django.conf import settings
from os import mkdir


def startup():
    if not settings.HLS_FOLDER.exists():
        mkdir(settings.HLS_FOLDER)
    
    if not settings.RECORD_FOLDER.exists():
        mkdir(settings.RECORD_FOLDER)


startup()