# Generated by Django 4.2.7 on 2024-01-08 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_project_application_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='projectId',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]