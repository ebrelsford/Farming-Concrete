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
            name='SmartsAndSkills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('participants', models.IntegerField(verbose_name='number of participants')),
                ('skills_shared', models.IntegerField(null=True, verbose_name='# of skills shared', blank=True)),
                ('skills_shared_examples', models.CharField(max_length=200, null=True, verbose_name='examples of skills shared', blank=True)),
                ('concepts_shared', models.IntegerField(null=True, verbose_name='# of concepts shared', blank=True)),
                ('concepts_shared_examples', models.CharField(max_length=200, null=True, verbose_name='examples of concepts shared', blank=True)),
                ('projects_proposed', models.IntegerField(null=True, verbose_name='# of projects proposed', blank=True)),
                ('projects_proposed_examples', models.CharField(max_length=200, null=True, verbose_name='examples of projects proposed', blank=True)),
                ('ideas_to_learn', models.IntegerField(null=True, verbose_name='# of ideas to learn', blank=True)),
                ('ideas_to_learn_examples', models.CharField(max_length=200, null=True, verbose_name='examples of ideas to learn', blank=True)),
                ('intentions_to_collaborate', models.IntegerField(null=True, verbose_name='# of intentions to collaborate', blank=True)),
                ('intentions_to_collaborate_examples', models.CharField(max_length=200, null=True, verbose_name='examples of intentions to collaborate', blank=True)),
                ('added_by', models.ForeignKey(related_name='skills_smartsandskills_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('updated_by', models.ForeignKey(related_name='skills_smartsandskills_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
