# Generated by Django 4.2.7 on 2024-06-20 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_bid_identity'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Submitted'), (1, 'In Review'), (2, 'Success'), (3, 'Denied')], default=0, null=True),
        ),
    ]