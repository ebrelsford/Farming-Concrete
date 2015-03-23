# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('farmingconcrete', '0003_auto_20150310_2118'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GardenGroupUserMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('group', models.ForeignKey(to='farmingconcrete.GardenGroup')),
                ('user_profile', models.ForeignKey(to='accounts.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
