# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compost', '0002_compostproductionweight_weight_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compostproductionweight',
            name='weight',
            field=models.DecimalField(null=True, verbose_name=b'weight (pounds)', max_digits=8, decimal_places=2, blank=True),
        ),
    ]
