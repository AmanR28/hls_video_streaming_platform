from django.shortcuts import redirect, render

from .forms import VideoForm
from .models import Video


def upload(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("status", video_id=form.instance.id)
        else:
            return render(request, "core/upload.html", {"form": form})

    return render(request, "core/upload.html", {"form": VideoForm()})


def status(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, "core/status.html", {"video": video})


def play(request, video_id):
    video = Video.objects.get(id=video_id)
    url = video.play.url.split("?")[0]
    return render(request, "core/play.html", {"video": video, "url": url})
