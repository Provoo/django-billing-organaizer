from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify
from django.contrib.postgres.fields import ArrayField
#google api credentials
# import pickle
# import base64
# from django.contrib import admin
# from oauth2client.contrib.django_util.models import CredentialsField


class UserDateUpdates(models.Model):
    UserID = models.ForeignKey(User, default=1)
    DateCreated = models.DateTimeField('Fecha de Creacion', null=True)
    DateUpdated = models.DateTimeField('Fecha de Actualizacion', null=True)


class Portafolio(models.Model):
    UserID = models.ForeignKey(User, default=1)
    Ruc = models.CharField(max_length=13)
    Nombre = models.CharField(max_length=50)

    def slug(self):
        return slugify(self.Ruc)

    def get_absolute_url(self):
        return reverse("user_dashboard", (), kwargs={
            'pk': self.UserID,
            'slug': self.slug
        })

    @property
    def total_gastos(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("totalGastosf"))["total"]

    @property
    def total_impuestos(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("totalImpuestos"))["total"]

    @property
    def total_portafolio(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("totalDocumento"))["total"]

    @property
    def total_comida(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("deducible_comida"))["total"]

    @property
    def total_salud(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("deducible_salud"))["total"]

    @property
    def total_vestimenta(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("deducible_vestimenta"))["total"]

    @property
    def total_educacion(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("deducible_educacion"))["total"]

    @property
    def total_vivienda(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("deducible_vivienda"))["total"]

    @property
    def total_no_deducible(self):
        return documento.objects.filter(
            rucDocumento=self.pk).aggregate(total=Sum("no_deducible"))["total"]

    def __str__(self):
        return '%s %s' % (self.UserID, self.Ruc)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'documents/{0}/{1}'.format(instance.rucDocumento, filename)

class documento(models.Model):
    rucDocumento = models.ForeignKey(Portafolio, default=1)
    nombreDocumento = models.CharField(max_length=100)
    numeroDeDocumento = models.CharField(max_length=30)
    RucEmisor = models.CharField(max_length=13)
    NombreEmisor = models.CharField(max_length=255)
    DireccionEmisor = models.CharField(max_length=255)
    fecha = models.DateTimeField('Fecha del documento')
    Impuesto = models.DecimalField(max_digits=4, decimal_places=2)
    totalGastosf = models.DecimalField(max_digits=20, decimal_places=2)
    totalImpuestos = models.DecimalField(max_digits=20, decimal_places=2)
    totalDocumento = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_vestimenta = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_educacion = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_comida = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_salud = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_vivienda = models.DecimalField(max_digits=20, decimal_places=2)
    tags = ArrayField(models.CharField(max_length=200), blank=True)
    no_deducible = models.DecimalField(max_digits=20, decimal_places=2)
    archivo = models.FileField(upload_to=user_directory_path, blank=True)
    def __str__(self):
        return '%s %s' % (self.rucDocumento, self.nombreDocumento)


def user_directory_error_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'documents/{0}/{1}'.format(instance.user_documento, filename)


class documento_error(models.Model):
    user_documento = models.ForeignKey(User)
    file_dcoumento = models.FileField(upload_to=user_directory_error_path)


    def slug(self):
        return slugify(self.rucDocumento)

    def __str__(self):
        return '%s %s' % (self.user_documento, self.file_dcoumento)
