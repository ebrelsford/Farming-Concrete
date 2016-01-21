# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landfilldiversion', '0002_auto_20151216_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landfilldiversionweight',
            name='weight',
        ),
    ]
