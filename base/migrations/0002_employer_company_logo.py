# Generated by Django 4.2.7 on 2024-03-02 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_logos'),
        ),
    ]
