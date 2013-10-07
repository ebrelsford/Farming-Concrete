from django.contrib import admin

from .models import ProgramFeature


class ProgramFeatureAdmin(admin.ModelAdmin):
    fields = ('name', 'universal',)
    list_display = ('name', 'universal',)


admin.site.register(ProgramFeature, ProgramFeatureAdmin)
