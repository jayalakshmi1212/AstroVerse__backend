# Generated by Django 5.1.3 on 2025-01-09 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
