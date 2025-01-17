# Generated by Django 5.0.6 on 2024-07-07 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="quality",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="video",
            name="thumbnail",
            field=models.ImageField(blank=True, null=True, upload_to="thumbnails"),
        ),
    ]
