# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gardener',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('added_by', models.ForeignKey(related_name='harvestcount_gardener_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(to='farmingconcrete.Garden')),
                ('updated_by', models.ForeignKey(related_name='harvestcount_gardener_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Harvest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('weight', models.DecimalField(verbose_name=b'weight (pounds)', max_digits=6, decimal_places=2)),
                ('plants', models.IntegerField(null=True, blank=True)),
                ('area', models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)),
                ('harvested', models.DateField(null=True, blank=True)),
                ('reportable', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(related_name='harvestcount_harvest_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('crop', models.ForeignKey(to='crops.Crop', null=True)),
                ('crop_variety', models.ForeignKey(blank=True, to='crops.Variety', null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('gardener', models.ForeignKey(to='harvestcount.Gardener')),
                ('updated_by', models.ForeignKey(related_name='harvestcount_harvest_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
