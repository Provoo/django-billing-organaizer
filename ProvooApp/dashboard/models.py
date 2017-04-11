from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify
#google api credentials
import pickle
import base64
from django.contrib import admin
from oauth2client.contrib.django_util.models import CredentialsField

class Portafolio(models.Model):
    UserID = models.ForeignKey(User)
    Ruc = models.CharField(max_length=13, primary_key=True)
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
            rucDocumento=self.Ruc).aggregate(total=Sum("totalGastosf"))["total"]

    @property
    def total_impuestos(self):
        return documento.objects.filter(
            rucDocumento=self.Ruc).aggregate(total=Sum("totalImpuestos"))["total"]

    @property
    def total_portafolio(self):
        return documento.objects.filter(
            rucDocumento=self.Ruc).aggregate(total=Sum("totalDocumento"))["total"]

    @property
    def total_vestimenta(self):
        return documento.objects.filter(
            rucDocumento=self.Ruc).aggregate(total=Sum("deducible_vestimenta"))["total"]

    @property
    def total_educacion(self):
        return documento.objects.filter(
            rucDocumento=self.Ruc).aggregate(total=Sum("deducible_educacion"))["total"]

    @property
    def total_comida(self):
        return documento.objects.filter(
            rucDocumento=self.Ruc).aggregate(total=Sum("deducible_comida"))["total"]

    @property
    def total_salud(self):
        return documento.objects.filter(
            rucDocumento=self.Ruc).aggregate(total=Sum("deducible_salud"))["total"]

    @property
    def total_no_deducible(self):
        return documento.objects.filter(
            rucDocumento=self.Ruc).aggregate(total=Sum("no_deducible"))["total"]

    def __str__(self):
        return '%s %s' % (self.UserID, self.Ruc)


class documento(models.Model):
    rucDocumento = models.ForeignKey(Portafolio)
    numeroDeDocumento = models.CharField(max_length=30)
    RucEmisor = models.CharField(max_length=13)
    NombreEmisor = models.CharField(max_length=50)
    DireccionEmisor = models.CharField(max_length=50)
    fecha = models.DateTimeField('Fecha del documento')
    totalGastosf = models.DecimalField(max_digits=20, decimal_places=2)
    totalImpuestos = models.DecimalField(max_digits=20, decimal_places=2)
    totalDocumento = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_vestimenta = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_educacion = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_comida = models.DecimalField(max_digits=20, decimal_places=2)
    deducible_salud = models.DecimalField(max_digits=20, decimal_places=2)
    no_deducible = models.DecimalField(max_digits=20, decimal_places=2)
    archivo = models.FileField(upload_to='documents/')

    def slug(self):
        return slugify(self.rucDocumento)

    def __str__(self):
        return '%s %s' % (self.rucDocumento, self.numeroDeDocumento)


#google api models for credentials
class CredentialsModel(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    credential = CredentialsField()


class CredentialsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CredentialsModel, CredentialsAdmin)
