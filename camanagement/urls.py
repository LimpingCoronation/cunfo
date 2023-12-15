from django.urls import path
from .views import add_cam, launch_hls, launch_record
from common.ip_filter import ip_filter

app_name = 'camanagement'

urlpatterns = [
    path('add_cam/', ip_filter(add_cam), name='add_cam'),
    path('launch_hls/', ip_filter(launch_hls), name='launch_hls'),
    path('launch_record/', ip_filter(launch_record), name='launch_record'),
]
