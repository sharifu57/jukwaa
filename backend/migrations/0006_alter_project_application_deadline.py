# Generated by Django 4.2.7 on 2024-01-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_project_application_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='application_deadline',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
