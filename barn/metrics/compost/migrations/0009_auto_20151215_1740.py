# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compost', '0008_remove_compostproductionvolume_volume'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compostproductionvolume',
            old_name='volume_new',
            new_name='volume',
        ),
    ]
