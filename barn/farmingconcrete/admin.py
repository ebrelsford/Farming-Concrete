from django.contrib import admin

from .models import Garden, GardenGroup, GardenType


class GardenAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'neighborhood', 'borough', 'city', 'state',)
    list_filter = ('type', 'borough', 'neighborhood', 'state',)
    search_fields = ('name', 'neighborhood', 'borough',)


class GardenGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_open', 'added_by',)
    search_fields = ('name', 'description',)
    readonly_fields = ('gardens',)


admin.site.register(Garden, GardenAdmin)
admin.site.register(GardenGroup, GardenGroupAdmin)
admin.site.register(GardenType)
