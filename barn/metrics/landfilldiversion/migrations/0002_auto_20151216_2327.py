# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('landfilldiversion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='landfilldiversionweight',
            name='weight_new',
            field=units.models.WeightField(measurement_class='Mass', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='landfilldiversionweight',
            name='weight',
            field=models.DecimalField(null=True, verbose_name=b'weight (pounds)', max_digits=8, decimal_places=2, blank=True),
        ),
    ]