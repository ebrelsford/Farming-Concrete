# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compost', '0004_remove_compostproductionweight_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compostproductionweight',
            old_name='weight_new',
            new_name='weight',
        ),
    ]
