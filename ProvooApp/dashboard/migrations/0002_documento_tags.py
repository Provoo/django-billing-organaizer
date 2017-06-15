# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 21:01
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=[], size=None),
            preserve_default=False,
        ),
    ]
