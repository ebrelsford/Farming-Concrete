from harvestcount.models import Gardener, Harvest
from django.contrib import admin

class GardenerAdmin(admin.ModelAdmin):
    list_display = ('name', 'garden',)
    search_fields = ('name', 'garden__name',)

class HarvestAdmin(admin.ModelAdmin):
    fields = ('variety', 'weight', 'plants', 'reportable',)
    list_display = ('variety', 'weight', 'plants', 'gardener', 'harvested', 'reportable',)
    list_filter = ('harvested', 'reportable',)
    search_fields = ('variety__name', 'gardener__name', 'gardener__garden__name',)

    def mark_as_unreportable(self, request, queryset):
        """mark a set of varieties as unreportable"""
        rows = queryset.update(reportable=False)
        if rows == 1:
            bit = "1 harvest"
        else:
            bit = "%s harvests" % rows
        self.message_user(request, "%s marked as unreportable" % bit) 

    actions = (mark_as_unreportable,)

admin.site.register(Gardener, GardenerAdmin)
admin.site.register(Harvest, HarvestAdmin)
