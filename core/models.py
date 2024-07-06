import datetime
import os
import uuid

from django.db import models
from django.forms import ValidationError


def generate_video_path(instance, filename):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    name = f"{filename.split('.')[0][:9]}_{timestamp}.{filename.split('.')[-1]}"
    return os.path.join(str(instance.id), name)


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to=generate_video_path)

    def clean(self) -> None:
        video = self.video
        if (not video) or (not video.file):
            raise ValidationError("No video file")
        if not video.file.content_type.startswith("video/"):
            raise ValidationError("File is not a video")
        return super().clean()
