# Generated by Django 5.1.3 on 2024-11-26 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_user_otp_user_otp_generated_at_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='document_tutor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
