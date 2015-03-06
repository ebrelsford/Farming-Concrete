# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='country',
            field=models.CharField(max_length=128, null=True, verbose_name='country', blank=True),
            preserve_default=True,
        ),
    ]
