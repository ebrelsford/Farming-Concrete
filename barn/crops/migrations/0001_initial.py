# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('needs_moderation', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(related_name='crops_crop_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='crops_crop_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'permissions': (('add_crop_unmoderated', 'Can add crops without moderation'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Variety',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('needs_moderation', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(related_name='crops_variety_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('crop', models.ForeignKey(to='crops.Crop')),
                ('updated_by', models.ForeignKey(related_name='crops_variety_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Varieties',
                'permissions': (('add_variety_unmoderated', 'Can add varieties without moderation'),),
            },
            bases=(models.Model,),
        ),
    ]
