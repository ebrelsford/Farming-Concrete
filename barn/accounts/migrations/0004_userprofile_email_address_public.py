# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150407_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_address_public',
            field=models.BooleanField(default=False),
        ),
    ]
