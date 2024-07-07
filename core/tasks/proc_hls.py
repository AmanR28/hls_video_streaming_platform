import os
import subprocess
from celery import shared_task

from . import shared


@shared_task
def proc_hls_360(id):
    video = shared.get_obj(id)
    # if video.quality < 360:
    # return

    path = shared.download_video(video)

    dir = f"./media/{id}_360/"
    shared.create_folder(dir)

    cmd = f"ffmpeg -hide_banner -y -i {path} -vf scale=w=640:h=360:force_original_aspect_ratio=decrease -c:a aac -ar 48000 -c:v h264 -profile:v main -crf 20 -sc_threshold 0 -g 48 -keyint_min 48 -hls_time 6 -hls_playlist_type vod  -b:v 800k -maxrate 856k -bufsize 1200k -b:a 96k {dir}/index.m3u8"
    result = subprocess.run(cmd, shell=True)

    shared.upload_folder_to_s3(dir, id + "/360")
    video.q360 = id + "/360/index.m3u8"
    video.save()


@shared_task
def proc_hls_720(id):
    video = shared.get_obj(id)
    # if video.quality < 720:
    # return

    path = shared.download_video(video)

    dir = f"./media/{id}_720/"
    shared.create_folder(dir)

    cmd = f"ffmpeg -hide_banner -y -i {path} -vf scale=w=1280:h=720:force_original_aspect_ratio=decrease -c:a aac -ar 48000 -c:v h264 -profile:v main -crf 20 -sc_threshold 0 -g 48 -keyint_min 48 -hls_time 6 -hls_playlist_type vod -b:v 2800k -maxrate 2996k -bufsize 4200k -b:a 128k {dir}/index.m3u8"
    result = subprocess.run(cmd, shell=True)

    shared.upload_folder_to_s3(dir, id + "/720")
    video.q720 = id + "/720/index.m3u8"
    video.save()
