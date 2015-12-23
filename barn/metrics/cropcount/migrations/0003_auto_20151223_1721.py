# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropcount', '0002_auto_20151222_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='length',
        ),
        migrations.RemoveField(
            model_name='box',
            name='width',
        ),
    ]
