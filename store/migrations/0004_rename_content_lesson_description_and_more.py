# Generated by Django 5.1.3 on 2024-12-04 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_course_lesson'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='content',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='video',
            new_name='video_url',
        ),
    ]
