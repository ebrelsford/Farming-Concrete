# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvestcount', '0003_remove_harvest_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='harvest',
            old_name='weight_new',
            new_name='weight',
        ),
    ]
