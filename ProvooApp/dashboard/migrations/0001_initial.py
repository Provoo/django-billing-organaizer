# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import dashboard.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='documento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreDocumento', models.CharField(max_length=50)),
                ('numeroDeDocumento', models.CharField(max_length=30)),
                ('RucEmisor', models.CharField(max_length=13)),
                ('NombreEmisor', models.CharField(max_length=100)),
                ('DireccionEmisor', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(verbose_name='Fecha del documento')),
                ('Impuesto', models.DecimalField(decimal_places=2, max_digits=4)),
                ('totalGastosf', models.DecimalField(decimal_places=2, max_digits=20)),
                ('totalImpuestos', models.DecimalField(decimal_places=2, max_digits=20)),
                ('totalDocumento', models.DecimalField(decimal_places=2, max_digits=20)),
                ('deducible_vestimenta', models.DecimalField(decimal_places=2, max_digits=20)),
                ('deducible_educacion', models.DecimalField(decimal_places=2, max_digits=20)),
                ('deducible_comida', models.DecimalField(decimal_places=2, max_digits=20)),
                ('deducible_salud', models.DecimalField(decimal_places=2, max_digits=20)),
                ('deducible_vivienda', models.DecimalField(decimal_places=2, max_digits=20)),
                ('no_deducible', models.DecimalField(decimal_places=2, max_digits=20)),
                ('archivo', models.FileField(upload_to=dashboard.models.user_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='documento_error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_dcoumento', models.FileField(upload_to=dashboard.models.user_directory_error_path)),
                ('user_documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Portafolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ruc', models.CharField(max_length=13)),
                ('Nombre', models.CharField(max_length=50)),
                ('UserID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='documento',
            name='rucDocumento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Portafolio'),
        ),
    ]
