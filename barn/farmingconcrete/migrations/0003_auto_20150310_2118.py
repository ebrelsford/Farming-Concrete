# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0002_garden_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='zip',
            field=models.CharField(max_length=16, null=True, verbose_name='postal code', blank=True),
            preserve_default=True,
        ),
    ]
