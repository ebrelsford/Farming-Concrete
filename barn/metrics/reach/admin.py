from django.contrib import admin

from .models import ProgramFeature


class ProgramFeatureAdmin(admin.ModelAdmin):
    fields = ('name', 'order', 'universal',)
    list_display = ('name', 'order', 'universal',)


admin.site.register(ProgramFeature, ProgramFeatureAdmin)
