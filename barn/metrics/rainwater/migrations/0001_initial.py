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
            name='RainwaterHarvest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('roof_length', models.DecimalField(verbose_name='roof length (feet)', max_digits=10, decimal_places=2)),
                ('roof_width', models.DecimalField(verbose_name='roof width (feet)', max_digits=10, decimal_places=2)),
                ('volume', models.DecimalField(null=True, verbose_name='volume (gallons)', max_digits=10, decimal_places=2, blank=True)),
                ('recorded_start', models.DateField(help_text='The beginning of the date range for this record', verbose_name='recorded start')),
                ('added_by', models.ForeignKey(related_name='rainwater_rainwaterharvest_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('updated_by', models.ForeignKey(related_name='rainwater_rainwaterharvest_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
