# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landfilldiversion', '0006_remove_landfilldiversionvolume_volume'),
    ]

    operations = [
        migrations.RenameField(
            model_name='landfilldiversionvolume',
            old_name='volume_new',
            new_name='volume',
        ),
    ]
