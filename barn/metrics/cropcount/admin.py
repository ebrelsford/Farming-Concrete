from django.contrib import admin

from .models import Patch


class PatchAdmin(admin.ModelAdmin):
    fields = ('box', 'crop', 'quantity', 'units', 'added_by', 'added',
              'updated_by', 'updated')
    list_display = ('box', 'crop', 'quantity', 'units', 'added_by', 'added',)
    readonly_fields = ('added', 'added_by', 'box', 'garden', 'updated', 'crop',)


admin.site.register(Patch, PatchAdmin)
