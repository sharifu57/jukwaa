# Generated by Django 4.2.7 on 2024-03-24 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_employer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('update', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]