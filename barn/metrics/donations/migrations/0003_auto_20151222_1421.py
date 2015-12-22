# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import units.models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_auto_20151222_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='pounds',
        ),
        migrations.AlterField(
            model_name='donation',
            name='weight',
            field=units.models.WeightField(measurement_class='Mass', null=True),
        ),
    ]
