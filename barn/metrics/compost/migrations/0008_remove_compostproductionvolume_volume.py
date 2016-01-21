# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compost', '0007_auto_20151214_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compostproductionvolume',
            name='volume',
        ),
    ]
