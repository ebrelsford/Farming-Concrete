# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('compost', '0006_auto_20151207_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='compostproductionvolume',
            name='volume_new',
            field=units.models.VolumeField(measurement_class='Volume', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='compostproductionvolume',
            name='volume',
            field=models.DecimalField(null=True, verbose_name=b'volume (gallons)', max_digits=8, decimal_places=2, blank=True),
        ),
    ]
