from django.urls import path
from .views import get_hls_playlist, get_hls_videoplayer, get_hls_video

app_name = 'hls'

urlpatterns = [
    path('<uuid:cam_uuid>/', get_hls_playlist, name='hls_playlist'),
    path('see/<uuid:cam_uuid>/', get_hls_videoplayer, name='hls_playlist'),
    path('<uuid:cam_uuid>/<str:filename>/', get_hls_video, name='hls_video'),
]
