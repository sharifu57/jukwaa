# Generated by Django 4.2.7 on 2023-12-25 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='duration',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
