# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-01 17:31
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20170707_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='portafolio',
            name='Tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=[], size=None),
            preserve_default=False,
        ),
    ]
