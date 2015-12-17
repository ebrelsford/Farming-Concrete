# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landfilldiversion', '0003_remove_landfilldiversionweight_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='landfilldiversionweight',
            old_name='weight_new',
            new_name='weight',
        ),
    ]
