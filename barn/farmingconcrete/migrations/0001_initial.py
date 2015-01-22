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
            name='Garden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('share_name', models.BooleanField(default=False, help_text="Share the garden's name in publicly available data.", verbose_name='share garden name')),
                ('share_location', models.BooleanField(default=False, help_text="Share the garden's location in publicly available data.", verbose_name='share garden location')),
                ('name', models.CharField(max_length=512, verbose_name=b'garden name')),
                ('gardenid', models.CharField(max_length=64, null=True, blank=True)),
                ('address', models.CharField(max_length=64, verbose_name=b'address')),
                ('city', models.CharField(max_length=128, null=True, verbose_name='city', blank=True)),
                ('state', models.CharField(max_length=128, null=True, verbose_name='state', blank=True)),
                ('borough', models.CharField(blank=True, max_length=32, null=True, choices=[(b'Brooklyn', b'Brooklyn'), (b'Bronx', b'Bronx'), (b'Manhattan', b'Manhattan'), (b'Queens', b'Queens'), (b'Staten Island', b'Staten Island')])),
                ('neighborhood', models.CharField(max_length=64, null=True, blank=True)),
                ('zip', models.CharField(max_length=16, null=True, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('has_metric_records', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('can_edit_any_garden', 'Can edit any garden'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GardenGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GardenGroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('garden', models.ForeignKey(to='farmingconcrete.Garden')),
                ('group', models.ForeignKey(to='farmingconcrete.GardenGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GardenType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('short_name', models.CharField(max_length=32)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gardengroup',
            name='gardens',
            field=models.ManyToManyField(to='farmingconcrete.Garden', through='farmingconcrete.GardenGroupMembership'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='garden',
            name='type',
            field=models.ForeignKey(to='farmingconcrete.GardenType'),
            preserve_default=True,
        ),
    ]
