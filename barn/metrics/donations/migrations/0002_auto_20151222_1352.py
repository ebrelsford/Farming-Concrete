# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='weight',
            field=units.models.WeightField(measurement_class='Mass', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pounds',
            field=models.DecimalField(null=True, verbose_name='pounds donated', max_digits=10, decimal_places=2, blank=True),
        ),
    ]
