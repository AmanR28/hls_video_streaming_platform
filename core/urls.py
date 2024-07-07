from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.upload),
    path("status/<uuid:video_id>/", views.status, name="status"),
    path("play/<uuid:video_id>/", views.play, name="play"),
]
