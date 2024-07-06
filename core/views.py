from django.shortcuts import redirect, render

from .forms import VideoForm


def upload(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect("status", video_id=form.instance.id)
            # else:
            return render(request, "core/upload.html", {"form": form})

    return render(request, "core/upload.html", {"form": VideoForm()})
