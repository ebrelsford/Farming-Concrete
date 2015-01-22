# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0001_initial'),
        ('harvestcount', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GardenMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('email_preferences', models.CharField(default=b'all', max_length=50, choices=[(b'all', b'all'), (b'none', b'none')])),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(to='farmingconcrete.Garden')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invite_count', models.PositiveIntegerField(default=0)),
                ('garden_types', models.ManyToManyField(to='farmingconcrete.GardenType', null=True, blank=True)),
                ('gardener', models.ForeignKey(blank=True, to='harvestcount.Gardener', null=True)),
                ('gardens', models.ManyToManyField(to='farmingconcrete.Garden', null=True, through='accounts.GardenMembership', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gardenmembership',
            name='user_profile',
            field=models.ForeignKey(to='accounts.UserProfile'),
            preserve_default=True,
        ),
    ]
