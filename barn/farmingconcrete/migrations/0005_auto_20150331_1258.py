# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0004_gardengroup_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='gardengroupmembership',
            name='status',
            field=models.CharField(default=b'active', max_length=20, choices=[(b'active', b'active'), (b'pending_requested', b'pending: requested'), (b'pending_invited', b'pending: invited')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gardengroup',
            name='is_open',
            field=models.BooleanField(default=False, help_text='Can any garden join the group, or are they required to get permission first?', verbose_name='is open'),
            preserve_default=True,
        ),
    ]
