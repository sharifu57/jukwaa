# Generated by Django 4.2.7 on 2024-01-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_project_application_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='application_deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]