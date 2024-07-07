from .proc_quality_template import proc_quality_template


def process_video(id):
    print("Processing video...", id)
    proc_quality_template.delay(id)
