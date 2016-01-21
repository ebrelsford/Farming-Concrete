# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropcount', '0003_auto_20151223_1721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='box',
            old_name='length_new',
            new_name='length',
        ),
        migrations.RenameField(
            model_name='box',
            old_name='width_new',
            new_name='width',
        ),
    ]
