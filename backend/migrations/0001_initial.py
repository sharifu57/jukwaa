# Generated by Django 4.2.7 on 2024-08-06 13:59

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
                ('price_from', models.CharField(blank=True, max_length=300, null=True)),
                ('price_to', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('update', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
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
                ('currency', models.IntegerField(blank=True, choices=[(1, 'TZS'), (2, 'Dollar')], default=1, null=True)),
                ('payment_type', models.IntegerField(blank=True, choices=[(1, 'pay_by_hour'), (2, 'pay_fixed_price')], null=True)),
                ('application_deadline', models.DateField(blank=True, null=True)),
                ('amount', models.CharField(blank=True, max_length=300, null=True)),
                ('projectId', models.CharField(blank=True, max_length=300, null=True)),
                ('size', models.IntegerField(blank=True, choices=[(1, 'Small'), (2, 'Medium')], null=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'New'), (1, 'Pending'), (2, 'In Review'), (3, 'Approved'), (4, 'Rejected'), (5, 'On Going'), (6, 'Completed'), (7, 'Closed')], default=0, null=True)),
                ('payment_status', models.IntegerField(blank=True, choices=[(0, 'Not Paid'), (1, 'Paid')], default=0, null=True)),
                ('project_file', models.FileField(blank=True, null=True, upload_to='projects/')),
                ('is_applied', models.BooleanField(blank=True, default=False, null=True)),
                ('budget', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.budget')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='base.category')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('duration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.duration')),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.employer')),
                ('experience', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.experience')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.location')),
                ('skills', models.ManyToManyField(blank=True, null=True, to='base.skill')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('update', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('proposal', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Submitted'), (1, 'In Review'), (2, 'Success'), (3, 'Denied')], default=0, null=True)),
                ('identity', models.CharField(blank=True, max_length=30, null=True)),
                ('is_accepted', models.BooleanField(blank=True, default=False, null=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('duration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.duration')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bids', to='backend.project')),
            ],
            options={
                'verbose_name': 'Bid',
                'verbose_name_plural': 'Bids',
            },
        ),
    ]
