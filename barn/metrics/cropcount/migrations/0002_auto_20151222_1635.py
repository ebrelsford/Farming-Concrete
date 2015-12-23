# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('cropcount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='length_new',
            field=units.models.DistanceField(measurement_class='Distance', null=True),
        ),
        migrations.AddField(
            model_name='box',
            name='width_new',
            field=units.models.DistanceField(measurement_class='Distance', null=True),
        ),
        migrations.AlterField(
            model_name='box',
            name='length',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='box',
            name='width',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=1, blank=True),
        ),
    ]
