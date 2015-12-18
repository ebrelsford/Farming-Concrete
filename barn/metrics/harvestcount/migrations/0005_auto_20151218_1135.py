# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('harvestcount', '0004_auto_20151218_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harvest',
            name='weight',
            field=units.models.WeightField(measurement_class='Mass', null=True),
        ),
    ]
