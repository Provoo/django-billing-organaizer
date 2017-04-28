from django.contrib import admin
from DocumentReader.models import EnterprisesMetadataEcuador


# Register your models here.
def clone_object(modeladmin, request, queryset):
    for obj in queryset:
        obj.id = None
        obj.save()
    clone_object.short_description = "clone"


class CloneObject(admin.ModelAdmin):
    list_display = ['NameDocument']
    ordering = ['NameDocument']
    actions = [clone_object]


admin.site.register(EnterprisesMetadataEcuador, CloneObject)
