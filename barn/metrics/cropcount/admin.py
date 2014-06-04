from django.contrib import admin

from .models import Patch


class PatchAdmin(admin.ModelAdmin):
    fields = ('box', 'variety', 'plants', 'area', 'quantity', 'units',
              'added_by', 'added', 'updated_by', 'updated')
    list_display = ('box', 'variety', 'plants', 'area', 'quantity', 'units',
                    'added_by', 'added',)
    readonly_fields = ('added', 'added_by', 'box', 'garden', 'updated',
                       'variety',)


admin.site.register(Patch, PatchAdmin)
