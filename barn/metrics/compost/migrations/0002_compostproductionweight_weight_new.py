# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('compost', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compostproductionweight',
            name='weight_new',
            field=units.models.WeightField(measurement_class='Mass', null=True, blank=True),
        ),
    ]
