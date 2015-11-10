# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barndrips', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarnHundredRecordDrip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('lastchanged', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text=b'A unique name for this drip.', unique=True, max_length=255, verbose_name=b'Drip Name')),
                ('enabled', models.BooleanField(default=False)),
                ('from_email', models.EmailField(help_text=b'Set a custom from email.', max_length=254, null=True, blank=True)),
                ('from_email_name', models.CharField(help_text=b'Set a name for a custom from email.', max_length=150, null=True, blank=True)),
                ('subject_template', models.TextField(null=True, blank=True)),
                ('body_html_template', models.TextField(help_text=b'You will have settings and user in the context.', null=True, blank=True)),
                ('message_class', models.CharField(default=b'default', max_length=120, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
