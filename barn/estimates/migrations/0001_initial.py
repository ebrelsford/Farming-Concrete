# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0001_initial'),
        ('crops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstimatedCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estimated', models.DateField()),
                ('notes', models.TextField(null=True, blank=True)),
                ('should_be_used', models.BooleanField(default=True)),
                ('valid_start', models.DateField()),
                ('valid_end', models.DateField()),
                ('cost_per_pound', models.DecimalField(max_digits=6, decimal_places=2)),
                ('organic', models.BooleanField(default=True)),
                ('source', models.TextField(null=True, blank=True)),
                ('crop', models.ForeignKey(to='crops.Crop', null=True)),
                ('crop_variety', models.ForeignKey(blank=True, to='crops.Variety', null=True)),
                ('garden_type', models.ForeignKey(blank=True, to='farmingconcrete.GardenType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstimatedYield',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estimated', models.DateField()),
                ('notes', models.TextField(null=True, blank=True)),
                ('should_be_used', models.BooleanField(default=True)),
                ('valid_start', models.DateField()),
                ('valid_end', models.DateField()),
                ('pounds_per_plant', models.DecimalField(max_digits=6, decimal_places=2)),
                ('crop', models.ForeignKey(to='crops.Crop', null=True)),
                ('crop_variety', models.ForeignKey(blank=True, to='crops.Variety', null=True)),
                ('garden_type', models.ForeignKey(blank=True, to='farmingconcrete.GardenType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
