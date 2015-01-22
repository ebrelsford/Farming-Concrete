# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0001_initial'),
        ('harvestcount', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HoursByGeography',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('recorded_start', models.DateField(help_text='The beginning of the date range for this record', verbose_name='recorded start')),
                ('neighborhood_definition', models.TextField(null=True, blank=True)),
                ('in_half', models.PositiveIntegerField(default=0, verbose_name='1/2-hour pins "IN"')),
                ('in_whole', models.PositiveIntegerField(default=0, verbose_name='1-hour pins "IN"')),
                ('out_half', models.PositiveIntegerField(default=0, verbose_name='1/2-hour pins "OUT"')),
                ('out_whole', models.PositiveIntegerField(default=0, verbose_name='1-hour pins "OUT"')),
                ('photo', models.ImageField(help_text='The photo you took to record this', upload_to=b'participation_geography', null=True, verbose_name='photo', blank=True)),
                ('added_by', models.ForeignKey(related_name='participation_hoursbygeography_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('updated_by', models.ForeignKey(related_name='participation_hoursbygeography_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HoursByProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('added_by', models.ForeignKey(related_name='participation_hoursbyproject_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HoursByTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('recorded_start', models.DateField(help_text='The beginning of the date range for this record', verbose_name='recorded start')),
                ('task_other', models.CharField(max_length=200, null=True, verbose_name='What do the other tasks include?', blank=True)),
                ('added_by', models.ForeignKey(related_name='participation_hoursbytask_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('garden', models.ForeignKey(to='farmingconcrete.Garden')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours', models.PositiveIntegerField(verbose_name='hours')),
                ('gardener', models.ForeignKey(verbose_name='Participant', to='harvestcount.Gardener')),
                ('record', models.ForeignKey(to='participation.HoursByProject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours', models.PositiveIntegerField(verbose_name='count')),
                ('hours_by_task', models.ForeignKey(verbose_name='hours by task', to='participation.HoursByTask')),
                ('task', models.ForeignKey(verbose_name='task', to='participation.Task')),
            ],
            options={
                'ordering': ('task__name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hoursbytask',
            name='tasks',
            field=models.ManyToManyField(to='participation.Task', verbose_name='tasks', through='participation.TaskHours'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hoursbytask',
            name='updated_by',
            field=models.ForeignKey(related_name='participation_hoursbytask_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hoursbyproject',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='participation.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hoursbyproject',
            name='updated_by',
            field=models.ForeignKey(related_name='participation_hoursbyproject_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
