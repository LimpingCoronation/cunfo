from django.conf import settings
from camanagement.models import Camera
import os
import subprocess

get_ffmpeg_command = lambda rtsp_link, path, bitrate, quality, resolution: \
    f"ffmpeg -i {rtsp_link} -y -s {resolution} -c:v libx264 -b:v {bitrate}k -crf {quality} -f hls -hls_list_size 20 -hls_time 1 -hls_flags delete_segments {str(path.joinpath('stream.m3u8'))}"


def create_ffmpeg_translation(camera: Camera, bitrate, quality, resolution):
    path_to_folder = settings.HLS_FOLDER.joinpath(str(camera.uuid))

    if not path_to_folder.exists():
        os.mkdir(str(path_to_folder))

    cmd = get_ffmpeg_command(camera.rtsp_url, path_to_folder, bitrate, quality, resolution)

    ffmpeg_stream = subprocess.Popen(cmd.split(' '), shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, bufsize=0)

    return ffmpeg_stream.pid
