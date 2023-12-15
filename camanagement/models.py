from django.db import models


class Camera(models.Model):
    name = models.CharField(max_length=200)
    rtsp_url = models.URLField(max_length=1000)
    uuid = models.UUIDField()
     
    def __str__(self):
        return f"Camera: {self.name} <{self.rtsp_url}>"
    

class HLSTranslation(models.Model):
    pid = models.PositiveSmallIntegerField()
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)


class RTSPRecording(models.Model):
    duration = models.PositiveIntegerField()
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)
