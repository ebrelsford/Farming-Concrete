from harvestcount.models import Gardener, Harvest
from django.contrib import admin

class GardenerAdmin(admin.ModelAdmin):
    #fields = ('name', 'address', 'neighborhood', 'borough', 'zip', 'gardenid',)
    list_display = ('name', 'garden',)
    search_fields = ('name', 'garden__name',)

class HarvestAdmin(admin.ModelAdmin):
    fields = ('variety', 'weight', 'plants',)
    list_display = ('variety', 'weight', 'plants', 'gardener', 'harvested',)
    list_filter = ('harvested', 'variety__name',)
    search_fields = ('variety__name', 'gardener__name', 'gardener__garden__name',)

admin.site.register(Gardener, GardenerAdmin)
admin.site.register(Harvest, HarvestAdmin)


