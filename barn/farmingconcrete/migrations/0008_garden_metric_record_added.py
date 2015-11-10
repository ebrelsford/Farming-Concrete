# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0007_garden_metric_records_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='metric_record_added',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
