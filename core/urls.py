from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("status/<uuid:video_id>/", views.status, name="status"),
    path("play/<uuid:video_id>/", views.play, name="play"),
]
