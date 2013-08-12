from django.contrib import admin

from .models import Patch


class PatchAdmin(admin.ModelAdmin):
    readonly_fields = ('added', 'added_by', 'box', 'garden', 'updated',
                       'variety',)
    fields = ('box', 'variety', 'plants', 'area', 'added_by', 'added',
              'updated_by', 'updated')


admin.site.register(Patch, PatchAdmin)
