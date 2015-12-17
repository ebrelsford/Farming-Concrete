# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('landfilldiversion', '0004_auto_20151216_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='landfilldiversionvolume',
            name='volume_new',
            field=units.models.VolumeField(measurement_class='Volume', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='landfilldiversionvolume',
            name='volume',
            field=models.DecimalField(null=True, verbose_name=b'volume (gallons)', max_digits=8, decimal_places=2, blank=True),
        ),
    ]
