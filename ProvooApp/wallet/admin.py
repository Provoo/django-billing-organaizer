from django.contrib import admin
from .models import wallet
# Register your models here.


class walletAdmin(admin.ModelAdmin):
    list_display = (
        'UserID',
        'name',
        'description',
        'currency',
        'address',
        'balance')


admin.site.register(wallet, walletAdmin)
