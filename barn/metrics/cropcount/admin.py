from django.contrib import admin

from metrics.cropcount.models import Box, Patch


class BoxInline(admin.TabularInline):
    model = Box
    extra = 1
    fields = ('name', 'length', 'width')


class PatchAdmin(admin.ModelAdmin):
    readonly_fields = ('added', 'updated')
    fields = ('box', 'variety', 'plants', 'area', 'added_by', 'added',
              'updated_by', 'updated')


admin.site.register(Patch, PatchAdmin)
