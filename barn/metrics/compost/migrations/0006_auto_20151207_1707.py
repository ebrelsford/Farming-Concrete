# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('compost', '0005_auto_20151207_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compostproductionweight',
            name='weight',
            field=units.models.WeightField(default=0, measurement_class='Mass'),
            preserve_default=False,
        ),
    ]
