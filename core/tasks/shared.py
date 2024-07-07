from core.models import Video
import time
import os
import boto3

import hls.settings as settings

s3_client = boto3.client(
    "s3", endpoint_url=settings.AWS_S3_ENDPOINT_URL, verify=settings.AWS_S3_VERIFY
)


def upload_to_s3(key, path):
    s3_client.upload_file(path, settings.AWS_STORAGE_BUCKET_NAME, key)


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_video(video):
    create_folder("./media/org/")

    name = f"{time.time()}_{video.id}"
    path = f"./media/org/{name}"

    f = open(path, "wb")
    f.write(video.video.read())
    f.close

    return path


def get_obj(id):
    return Video.objects.get(id=id)
