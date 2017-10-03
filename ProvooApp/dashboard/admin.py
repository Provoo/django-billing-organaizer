from django.contrib import admin
from dashboard.models import Portafolio, documento, documento_error, UserDateUpdates
# Register your models here.


class PortafolioAdmin(admin.ModelAdmin):
    list_display = (
        'UserID', 'Ruc', 'Nombre', 'total_gastos', 'total_impuestos',
        'total_portafolio', 'total_vestimenta', 'total_educacion',
        'total_comida', 'total_salud', 'total_no_deducible')


class DocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'rucDocumento', 'NombreEmisor', 'numeroDeDocumento', 'totalGastosf', 'totalImpuestos',
        'totalDocumento')


admin.site.register(Portafolio, PortafolioAdmin)
admin.site.register(documento, DocumentoAdmin)
admin.site.register(documento_error)
admin.site.register(UserDateUpdates)
