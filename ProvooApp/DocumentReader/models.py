from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models


class EnterprisesMetadataEcuador(models.Model):
    id = models.AutoField(primary_key=True)
    Country = models.CharField(max_length=40)
    NameDocument = models.CharField(max_length=40)
    IdDocument = models.CharField(max_length=40)
    Parser_Flag = models.IntegerField()
    Type_Document_Flag = models.IntegerField()
    Clienteid = models.CharField(max_length=40)
    EnterpriseId = models.CharField(max_length=40)
    EnterpriseName = models.CharField(max_length=40)
    EnterpriseComercialName = models.CharField(max_length=40)
    EnterpriseDateAuth = models.CharField(max_length=40)
    EnterpriseAddress = models.CharField(max_length=40)
    EnterpriseNoTax = models.CharField(max_length=40)
    EnterpriseTotalTax = models.CharField(max_length=40)
    EnterpriseTotalTax = models.CharField(max_length=40)
    EnterpriseTotal = models.CharField(max_length=40)
    EnterpriseFood = models.CharField(max_length=40)
    EnterpriseMed = models.CharField(max_length=40)
    EnterpriseClothes = models.CharField(max_length=40)
    EnterpriseEdu = models.CharField(max_length=40)
    EnterpriseHome = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % (self.NameDocument)
