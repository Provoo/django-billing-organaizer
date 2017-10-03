# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-03 21:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0008_auto_20171003_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDateUpdates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateCreated', models.DateTimeField(null=True, verbose_name='Fecha de Creacion')),
                ('DateUpdated', models.DateTimeField(null=True, verbose_name='Fecha de Actualizacion')),
                ('UserID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
