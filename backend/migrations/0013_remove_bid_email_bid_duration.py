# Generated by Django 4.2.7 on 2024-01-11 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_alter_bid_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='email',
        ),
        migrations.AddField(
            model_name='bid',
            name='duration',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]