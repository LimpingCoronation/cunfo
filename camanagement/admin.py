from django.contrib import admin
from .models import Camera, HLSTranslation, RTSPRecording

# Register your models here.
admin.site.register(Camera)
admin.site.register(HLSTranslation)
admin.site.register(RTSPRecording)