from django import forms
from dashboard.models import documento


class subirDocumento(forms.Form):
    model = documento
    fields = ('archivo',)
