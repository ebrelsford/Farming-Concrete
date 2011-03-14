from cropcount.models import Garden, Variety, Box, Patch
from django.contrib import admin

class BoxInline(admin.TabularInline):
    model = Box
    extra = 1
    fields = ('name', 'length', 'width')

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
admin.site.register(Patch)
