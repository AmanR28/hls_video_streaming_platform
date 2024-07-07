from celery import chain, group

from .proc_hls import proc_hls_360, proc_hls_720
from .proc_playlist import proc_playlist
from .proc_quality_template import proc_quality_template


def process_video(id):
    print("Processing video...", id)
    pre = proc_quality_template.si(id)
    gen = group(proc_hls_360.si(id), proc_hls_720.si(id))
    post = proc_playlist.si(id)
    chain(pre, gen, post)()
