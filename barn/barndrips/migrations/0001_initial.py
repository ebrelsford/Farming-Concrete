# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drip', '0003_auto_20150814_0724'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarnGardenDrip',
            fields=[
                ('drip_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='drip.Drip')),
            ],
            bases=('drip.drip',),
        ),
    ]
