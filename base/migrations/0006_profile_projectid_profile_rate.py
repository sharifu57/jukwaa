# Generated by Django 4.2.7 on 2024-01-08 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_profile_user_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='projectId',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='rate',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
