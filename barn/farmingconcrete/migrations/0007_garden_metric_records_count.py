# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0006_garden_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='metric_records_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
