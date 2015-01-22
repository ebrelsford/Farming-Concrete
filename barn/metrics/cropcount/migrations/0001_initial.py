# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('farmingconcrete', '0001_initial'),
        ('crops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32)),
                ('length', models.DecimalField(max_digits=4, decimal_places=1)),
                ('width', models.DecimalField(max_digits=4, decimal_places=1)),
                ('added_by', models.ForeignKey(related_name='cropcount_box_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(to='farmingconcrete.Garden')),
                ('updated_by', models.ForeignKey(related_name='cropcount_box_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Boxes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('quantity', models.DecimalField(max_digits=5, decimal_places=2)),
                ('units', models.CharField(max_length=15, choices=[(b'plants', b'plants'), (b'row feet', b'row feet'), (b'square feet', b'square feet')])),
                ('added_by', models.ForeignKey(related_name='cropcount_patch_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('box', models.ForeignKey(to='cropcount.Box')),
                ('crop', models.ForeignKey(to='crops.Crop', null=True)),
                ('crop_variety', models.ForeignKey(blank=True, to='crops.Variety', null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('updated_by', models.ForeignKey(related_name='cropcount_patch_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['crop'],
                'verbose_name_plural': 'Patches',
            },
            bases=(models.Model,),
        ),
    ]
