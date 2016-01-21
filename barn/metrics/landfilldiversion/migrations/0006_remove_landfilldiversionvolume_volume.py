# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landfilldiversion', '0005_auto_20151217_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landfilldiversionvolume',
            name='volume',
        ),
    ]
