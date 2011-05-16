from harvestcount.models import Gardener, Harvest
from django.contrib import admin

class GardenerAdmin(admin.ModelAdmin):
    #fields = ('name', 'address', 'neighborhood', 'borough', 'zip', 'gardenid',)
    list_display = ('name', 'garden',)
    search_fields = ('name', 'garden',)

class HarvestAdmin(admin.ModelAdmin):
    fields = ('variety', 'weight', 'plants',)
    list_display = ('variety', 'weight', 'plants',)

admin.site.register(Gardener, GardenerAdmin)
admin.site.register(Harvest, HarvestAdmin)


