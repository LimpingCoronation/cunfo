from django import forms
from .models import Camera


class CameraForm(forms.Form):
    name = forms.CharField(max_length=1000, widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter name of camera',
            'class': 'form-select mb-3',
            'aria-label': 'Name'
        }
    ))
    rtsp_url = forms.CharField(widget=forms.URLInput(
        attrs={
            'placeholder': 'Enter rtsp url of camera',
            'class': 'form-select mb-3',
            'aria-label': 'RTSP URL'
        }
    ))


class HLSForm(forms.Form):
    name = forms.ChoiceField(choices=[], 
        widget=forms.Select(attrs={
            'class': 'form-select mb-3',
            'aria-label': 'Select camera for HLS'
        }
    ))

    def __init__(self, *args, **kwargs):
        super(HLSForm, self).__init__(*args, **kwargs)
        self.fields['name'].choices = [(cam.name, cam.name) for cam in Camera.objects.all()]


class RecordForm(HLSForm):
    duration = forms.CharField(widget=forms.NumberInput(attrs={
            'placeholder': 'Enter duration of one fragment',
            'class': 'form-select mb-3',
            'aria-label': 'Select camera for HLS'
        }
    ))

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['duration'].label = "Duration in minutes:"