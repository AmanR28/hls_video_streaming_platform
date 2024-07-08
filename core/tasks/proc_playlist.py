from celery import shared_task

from django.conf import settings

from . import shared


@shared_task
def proc_playlist(id):
    video = shared.get_obj(id)

    if video.quality >= 720:
        shared.upload_to_s3(
            id + "/playlist.m3u8",
            str(settings.BASE_DIR) + "/core/static/playlist/hd.m3u8",
        )
        video.play = f"{id}/playlist.m3u8"  # type: ignore

    elif video.quality >= 360:
        shared.upload_to_s3(
            id + "/playlist.m3u8",
            str(settings.BASE_DIR) + "/core/static/playlist/sd.m3u8",
        )
        video.play = f"{id}/playlist.m3u8"  # type: ignore

    else:
        video.play = f"{id}/video"  # type: ignore

    video.save()
