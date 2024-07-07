import datetime
import os
import uuid

from django.db import models
from django.forms import ValidationError


def generate_video_path(instance, filename):
    return os.path.join(str(instance.id), "video")


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to=generate_video_path)
    quality = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def clean(self) -> None:
        video = self.video
        if (not video) or (not video.file):
            raise ValidationError("No video file")
        if not video.file.content_type.startswith("video/"):
            raise ValidationError("File is not a video")
        return super().clean()
