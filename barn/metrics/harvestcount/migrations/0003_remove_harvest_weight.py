# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvestcount', '0002_auto_20151217_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='harvest',
            name='weight',
        ),
    ]
