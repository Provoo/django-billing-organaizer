from django import forms
from dashboard.models import documento


class subirDocumentoManual(forms.Form):
    model = documento
    fields = (
        'rucDocumento',
        'nombreDocumento',
        'numeroDeDocumento',
        'RucEmisor',
        'NombreEmisor',
        'DireccionEmisor',
        'fecha',
        'Impuesto',
        'totalGastosf',
        'totalImpuestos',
        'totalDocumento',
        'deducible_vestimenta',
        'deducible_educacion',
        'deducible_comida',
        'deducible_salud',
        'deducible_vivienda',
        'tags',
        'no_deducible',
        'archivo'
        )
