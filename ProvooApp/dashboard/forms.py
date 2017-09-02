from django import forms
from django.contrib.admin import widgets

# from dashboard.models import documento


class uploadManualForm(forms.Form):
    NombreEmisor = forms.CharField(label='Nombre Emisor Factura', max_length=100)
    RucEmisor = forms.CharField(label='Ruc Emisor Factura', max_length=13)
    nombreDocumento = forms.CharField(label='Nombre del Destinatario', max_length=100)
    rucDocumento = forms.CharField(label=' RUC/CI del Destinatario ', max_length=13)
    numeroDeDocumento = forms.CharField(label='Numero de Factura', max_length=30)
    fecha = forms.CharField(label='Fecha', max_length=13)
    Impuesto = forms.DecimalField(label='Porcentaje de impuesto ejemplo 12', max_digits=4, decimal_places=2)
    totalGastosf = forms.DecimalField(label='Subtotal', max_digits=20, decimal_places=2)
    totalImpuestos = forms.DecimalField(label='Impuestos', max_digits=20, decimal_places=2)
    totalDocumento = forms.DecimalField(label='Total', max_digits=20, decimal_places=2)
    deducible_comida = forms.DecimalField(label='Deducibel Alimentacion', max_digits=20, decimal_places=2)
    deducible_salud = forms.DecimalField(label='Deducibel Salud', max_digits=20, decimal_places=2)
    deducible_vestimenta = forms.DecimalField(label='Deducibel Vestimenta', max_digits=20, decimal_places=2)
    deducible_educacion = forms.DecimalField(label='Deducibel Educacion', max_digits=20, decimal_places=2)
    deducible_vivienda = forms.DecimalField(label='Deducibel Vivienda', max_digits=20, decimal_places=2)
    no_deducible = forms.DecimalField(label='No Deducibel', max_digits=20, decimal_places=2)
    tags = forms.CharField(label='Tags Separado por comas', max_length=255)


class registerExpensesForm(forms.Form):
    Empresas = forms.CharField(label='Tags Separado por comas', max_length=255)
    tags = forms.CharField(label='Tags Separado por comas', max_length=255)

# class uploadManualForm(forms.ModelForm):
#     class Meta:
#         model = documento
#         fields = [
#             'nombreDocumento',
#             'numeroDeDocumento',
#             'RucEmisor',
#             'NombreEmisor',
#             'DireccionEmisor',
#             'fecha',
#             'Impuesto',
#             'totalGastosf',
#             'totalImpuestos',
#             'totalDocumento',
#             'deducible_vestimenta',
#             'deducible_educacion',
#             'deducible_comida',
#             'deducible_salud',
#             'deducible_vivienda',
#             'tags',
#             'no_deducible',
#             'archivo',
#         ]
