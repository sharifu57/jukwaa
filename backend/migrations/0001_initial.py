# Generated by Django 4.2.7 on 2023-12-25 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('update', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('price_from', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('price_to', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('update', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, choices=[(1, 'ASAP'), (2, 'Within a Week'), (3, 'A Month'), (4, 'Custom')], null=True)),
                ('currency', models.IntegerField(blank=True, choices=[(1, 'TZS'), (2, 'Dollar')], default=1, null=True)),
                ('payment_type', models.IntegerField(blank=True, choices=[(1, 'pay_by_hour'), (2, 'pay_fixed_price')], null=True)),
                ('amount', models.CharField(blank=True, max_length=300, null=True)),
                ('project_file', models.FileField(blank=True, null=True, upload_to='projects/')),
                ('budget', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.budget')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.category')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(blank=True, null=True, to='base.skill')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
