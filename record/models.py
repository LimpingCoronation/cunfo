from django.db import models
from camanagement.models import RTSPRecording

# Create your models here.
class Record(models.Model):
    filename = models.CharField(max_length=1000)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    record = models.ForeignKey(to=RTSPRecording, on_delete=models.DO_NOTHING)
