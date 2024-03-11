from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

resolution_validator = RegexValidator(r"^\d{1,5}x\d{1,5}")


class Camera(models.Model):
    name = models.CharField(max_length=200)
    rtsp_url = models.URLField(max_length=1000)
    uuid = models.UUIDField()
     
    def __str__(self):
        return f"Camera: {self.name} <{self.rtsp_url}>"
    

class HLSTranslation(models.Model):
    pid = models.PositiveIntegerField()
    resolution = models.CharField(max_length=11, validators=[resolution_validator])
    bitrate = models.PositiveIntegerField()
    quality = models.PositiveSmallIntegerField(default=18, validators=[MinValueValidator(0), MaxValueValidator(51)])
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)


class RTSPRecording(models.Model):
    pid = models.PositiveIntegerField()
    bitrate = models.PositiveIntegerField()
    quality = models.PositiveSmallIntegerField(default=18, validators=[MinValueValidator(0), MaxValueValidator(51)])
    duration = models.PositiveIntegerField()
    days = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(21)])
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)
