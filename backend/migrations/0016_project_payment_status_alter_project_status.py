# Generated by Django 4.2.7 on 2024-01-23 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_project_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='payment_status',
            field=models.IntegerField(blank=True, choices=[(0, 'Not Paid'), (1, 'Paid')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'New'), (1, 'Pending'), (2, 'In Review'), (3, 'Approved'), (4, 'Rejected')], default=0, null=True),
        ),
    ]
