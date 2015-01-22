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
            name='LookingGoodEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('total_participants', models.PositiveIntegerField(default=0, verbose_name='# of participants')),
                ('total_tags', models.PositiveIntegerField(default=0, verbose_name='# of tags')),
                ('items_tagged', models.PositiveIntegerField(default=0, verbose_name='# of items tagged')),
                ('added_by', models.ForeignKey(related_name='lookinggood_lookinggoodevent_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('updated_by', models.ForeignKey(related_name='lookinggood_lookinggoodevent_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LookingGoodItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='Tagged item')),
                ('tags', models.PositiveIntegerField(verbose_name='# of tags')),
                ('comments', models.TextField(verbose_name='Comments')),
                ('event', models.ForeignKey(verbose_name='event', to='lookinggood.LookingGoodEvent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LookingGoodPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=b'lookinggood_event', null=True, verbose_name='photo', blank=True)),
                ('caption', models.CharField(max_length=250, null=True, verbose_name='caption', blank=True)),
                ('event', models.ForeignKey(verbose_name='event', to='lookinggood.LookingGoodEvent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
