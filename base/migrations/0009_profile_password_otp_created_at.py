# Generated by Django 4.2.7 on 2024-08-05 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_profile_password_otp_profile_password_otp_is_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='password_otp_created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
