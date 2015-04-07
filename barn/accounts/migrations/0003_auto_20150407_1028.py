# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_gardengroupusermembership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='garden_types',
            field=models.ManyToManyField(to='farmingconcrete.GardenType', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gardens',
            field=models.ManyToManyField(to='farmingconcrete.Garden', through='accounts.GardenMembership', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
