# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20170324_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='nombreDocumento',
            field=models.CharField(default='Carlos', max_length=50),
            preserve_default=False,
        ),
    ]
