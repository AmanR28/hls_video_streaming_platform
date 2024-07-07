import subprocess
from celery import shared_task
from . import shared


def proc_quality(path):
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {path}"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    width, height = result.stdout.decode("utf-8").split("x")
    height = int(height)
    if height >= 1080:
        return 1080
    elif height >= 720:
        return 720
    elif height >= 480:
        return 480
    elif height >= 360:
        return 360
    return 0


def proc_thumbnail(id, path):
    dir = f"./media/{id}_thumbnail/"
    shared.create_folder(dir)

    out_path = dir + "thumbnail.jpg"
    cmd = f"ffmpeg -i {path} -ss 00:00:00.500 -vframes 1 {out_path}"
    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        raise Exception("Failed to generate thumbnail")

    key = f"{id}/thumbnail.jpg"
    shared.upload_to_s3(key, out_path)

    return "./" + key


@shared_task
def proc_quality_template(id):
    video = shared.get_obj(id)
    path = shared.download_video(video)

    quality = proc_quality(path)
    video.quality = quality
    video.save()

    thumbnail = proc_thumbnail(id, path)
    video.thumbnail = thumbnail  # type: ignore
    video.save()
