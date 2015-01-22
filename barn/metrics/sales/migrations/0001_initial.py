# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('farmingconcrete', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recorded', models.DateField(help_text='The date this was recorded', null=True, verbose_name='recorded', blank=True)),
                ('product', models.CharField(max_length=100, verbose_name='product')),
                ('unit', models.CharField(max_length=50, verbose_name='unit')),
                ('unit_price', models.DecimalField(verbose_name='unit price', max_digits=10, decimal_places=2)),
                ('units_sold', models.DecimalField(verbose_name='units sold', max_digits=10, decimal_places=2)),
                ('total_price', models.DecimalField(verbose_name='total price', max_digits=10, decimal_places=2)),
                ('added_by', models.ForeignKey(related_name='sales_sale_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('garden', models.ForeignKey(blank=True, to='farmingconcrete.Garden', help_text='The garden this refers to', null=True, verbose_name='garden')),
                ('updated_by', models.ForeignKey(related_name='sales_sale_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
