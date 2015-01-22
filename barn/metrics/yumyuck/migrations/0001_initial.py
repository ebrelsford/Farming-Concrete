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
            name='YumYuck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('yum_before', models.PositiveIntegerField(verbose_name='yums before')),
                ('yuck_before', models.PositiveIntegerField(verbose_name='yucks before')),
                ('yum_after', models.PositiveIntegerField(verbose_name='yums after')),
                ('yuck_after', models.PositiveIntegerField(verbose_name='yucks after')),
                ('added_by', models.ForeignKey(related_name='yumyuck_yumyuck_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('crop', models.ForeignKey(to='crops.Crop', null=True)),
                ('crop_variety', models.ForeignKey(blank=True, to='crops.Variety', null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('updated_by', models.ForeignKey(related_name='yumyuck_yumyuck_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
