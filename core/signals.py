import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import process_video
from .models import Video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance: Video, created, **kwargs):
    if created:
        process_video(str(instance.pk))
