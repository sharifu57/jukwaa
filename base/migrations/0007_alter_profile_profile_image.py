# Generated by Django 4.2.7 on 2024-04-22 19:12

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_profile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=base.models.profile_location),
        ),
    ]