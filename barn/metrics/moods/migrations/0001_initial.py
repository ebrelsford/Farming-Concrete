# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type', choices=[(b'positive', b'positive'), (b'negative', b'negative'), (b'neutral', b'neutral')])),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoodChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('recorded_start', models.DateField(help_text='When you started recording mood changes', verbose_name='recorded start')),
                ('added_by', models.ForeignKey(related_name='moods_moodchange_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoodCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField(verbose_name='count')),
                ('counted_time', models.CharField(max_length=25, verbose_name='counted time', choices=[(b'in', b'in'), (b'out', b'out')])),
                ('mood', models.ForeignKey(verbose_name='mood', to='moods.Mood')),
                ('mood_change', models.ForeignKey(verbose_name='mood change', to='moods.MoodChange')),
            ],
            options={
                'ordering': ('counted_time', 'mood__name'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='moodchange',
            name='mood_counts',
            field=models.ManyToManyField(to='moods.Mood', through='moods.MoodCount'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='moodchange',
            name='updated_by',
            field=models.ForeignKey(related_name='moods_moodchange_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
