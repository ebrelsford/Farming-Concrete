from farmingconcrete.models import Garden, Variety
from cropcount.admin import BoxInline
from django.contrib import admin

class GardenAdmin(admin.ModelAdmin):
    #fields = ('name', 'address', 'neighborhood', 'borough', 'zip', 'gardenid',)
    list_display = ('name', 'neighborhood', 'borough',)
    search_fields = ('name', 'neighborhood', 'borough',)
    inlines = (BoxInline,)

class VarietyAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)

admin.site.register(Garden, GardenAdmin)
admin.site.register(Variety, VarietyAdmin)

