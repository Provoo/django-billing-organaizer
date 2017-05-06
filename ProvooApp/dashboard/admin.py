
from django.contrib import admin
from dashboard.models import Portafolio, documento, documento_error
# Register your models here.


class PortafolioAdmin(admin.ModelAdmin):
    list_display = (
        'UserID', 'Ruc', 'Nombre', 'total_gastos', 'total_impuestos',
        'total_portafolio', 'total_vestimenta', 'total_educacion',
        'total_comida', 'total_salud', 'total_no_deducible')


admin.site.register(Portafolio, PortafolioAdmin)
admin.site.register(documento)
admin.site.register(documento_error)
