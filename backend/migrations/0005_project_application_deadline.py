# Generated by Django 4.2.7 on 2023-12-28 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_bid_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='application_deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]