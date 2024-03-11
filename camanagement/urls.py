from django.urls import path
from .views import add_cam, launch_hls, launch_record, camera_list, update_camera, delete_camera, processes_list, kill_proc
from common.ip_filter import ip_filter

app_name = 'camanagement'

urlpatterns = [
    path('add_cam/', ip_filter(add_cam), name='add_cam'),
    path('launch_hls/', ip_filter(launch_hls), name='launch_hls'),
    path('launch_record/', ip_filter(launch_record), name='launch_record'),
    path('cameras_list/', ip_filter(camera_list), name='cameras_list'),
    path('delete/<uuid:cam_uuid>', ip_filter(delete_camera), name='delete_cam'),
    path('update/<uuid:cam_uuid>', ip_filter(update_camera), name='update_cam'),
    path('procs/', ip_filter(processes_list), name='proc_list'),
    path('kill/<int:pid>', ip_filter(kill_proc), name='kill_proc'),
]
