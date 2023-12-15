from django.conf import settings
from camanagement.models import Camera
import os
import subprocess
from pathlib import Path

get_ffmpeg_command = lambda rtsp_link, path: \
    f"ffmpeg -i {rtsp_link} -y -s 1280x720 -c:v libx264 -b:v 800000 -f hls -x264-params keyint=15:min-keyint=15 -hls_list_size 20 -hls_time 1 -hls_flags delete_segments {str(path.joinpath('stream.m3u8'))}"


def create_ffmpeg_translation(camera: Camera):
    path_to_folder = settings.HLS_FOLDER.joinpath(str(camera.uuid))
    os.mkdir(str(path_to_folder))

    cmd = get_ffmpeg_command(camera.rtsp_url, path_to_folder)

    ffmpeg_stream = subprocess.Popen(cmd.split(' '), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return ffmpeg_stream.pid