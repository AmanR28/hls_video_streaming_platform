from core.models import Video
import time
import os
import glob
import boto3

import hls.settings as settings

s3_client = boto3.client(
    "s3", endpoint_url=settings.AWS_S3_ENDPOINT_URL, verify=settings.AWS_S3_VERIFY
)


def upload_to_s3(key, path):
    s3_client.upload_file(path, settings.AWS_STORAGE_BUCKET_NAME, key)


def upload_folder_to_s3(folder, key):
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            upload_to_s3(f"{key}/{os.path.basename(file)}", path)


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def remove_folder(path):
    files = glob.glob(path + "*")
    for f in files:
        os.remove(f)
    os.rmdir(path)


def download_video(video):
    dir = "./media/org/"
    create_folder(dir)

    name = f"{time.time()}_{video.id}"
    path = dir + name

    f = open(path, "wb")
    f.write(video.video.read())
    f.close

    return path


def delete_video(path):
    os.remove(path)


def get_obj(id):
    return Video.objects.get(id=id)
