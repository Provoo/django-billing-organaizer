# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-11 03:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_portafolio_totalgastos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portafolio',
            name='totalImpuestos',
        ),
    ]
