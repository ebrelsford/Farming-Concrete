from django.contrib import admin

from .models import Garden, GardenGroup, GardenType


class GardenAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'neighborhood', 'borough', 'city', 'state',)
    list_filter = ('type', 'borough', 'neighborhood', 'state',)
    search_fields = ('name', 'neighborhood', 'borough',)


admin.site.register(Garden, GardenAdmin)
admin.site.register(GardenGroup)
admin.site.register(GardenType)
