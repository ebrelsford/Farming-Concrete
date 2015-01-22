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
            name='ProgramFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='name')),
                ('order', models.PositiveIntegerField(default=0)),
                ('universal', models.BooleanField(default=True, help_text='This feature should be available to all gardens', verbose_name='universal')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgramReach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('name', models.CharField(max_length=300, verbose_name='program name')),
                ('recorded_start', models.DateField(verbose_name='program start')),
                ('hours_each_day', models.DecimalField(verbose_name='hours each day', max_digits=3, decimal_places=1)),
                ('collaborated_with_organization', models.BooleanField(default=False, verbose_name='Did you collaborate with another organization to host this program?')),
                ('collaboration_first', models.BooleanField(default=False, verbose_name='Was this the first time you worked together?')),
                ('age_10', models.IntegerField(null=True, verbose_name='# Under 10', blank=True)),
                ('age_10_14', models.IntegerField(null=True, verbose_name='# 10 to 14', blank=True)),
                ('age_15_19', models.IntegerField(null=True, verbose_name='# 15 to 19', blank=True)),
                ('age_20_24', models.IntegerField(null=True, verbose_name='# 20 to 24', blank=True)),
                ('age_25_34', models.IntegerField(null=True, verbose_name='# 25 to 34', blank=True)),
                ('age_35_44', models.IntegerField(null=True, verbose_name='# 35 to 44', blank=True)),
                ('age_45_54', models.IntegerField(null=True, verbose_name='# 45 to 54', blank=True)),
                ('age_55_64', models.IntegerField(null=True, verbose_name='# 55 to 64', blank=True)),
                ('age_65', models.IntegerField(null=True, verbose_name='65 and older', blank=True)),
                ('gender_male', models.IntegerField(null=True, verbose_name='# Male', blank=True)),
                ('gender_female', models.IntegerField(null=True, verbose_name='# Female', blank=True)),
                ('gender_other', models.IntegerField(null=True, verbose_name='# Other gender', blank=True)),
                ('zipcode_inside', models.IntegerField(null=True, verbose_name='# Within garden zip code', blank=True)),
                ('zipcode_outside', models.IntegerField(null=True, verbose_name='# Outside garden zip code', blank=True)),
                ('other_features', models.CharField(max_length=200, null=True, verbose_name='other features', blank=True)),
                ('added_by', models.ForeignKey(related_name='reach_programreach_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('features', models.ManyToManyField(help_text='Features this program included', to='reach.ProgramFeature', null=True, verbose_name='features', blank=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('updated_by', models.ForeignKey(related_name='reach_programreach_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
