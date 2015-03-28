# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0003_auto_20150310_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='gardengroup',
            name='is_open',
            field=models.BooleanField(default=False, help_text='Can anyone join the group, or are they required to get permission first?', verbose_name='is open'),
            preserve_default=True,
        ),
    ]
