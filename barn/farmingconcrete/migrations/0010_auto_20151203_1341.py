# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0009_garden_measurement_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='measurement_system',
            field=models.CharField(default=b'imperial', help_text='Pick the measurement system that will be used for this garden.', max_length=25, verbose_name='measurement system', choices=[(b'imperial', b'imperial'), (b'metric', b'metric')]),
        ),
    ]
