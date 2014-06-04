from django.contrib import admin

from .models import Gardener, Harvest


class GardenerAdmin(admin.ModelAdmin):
    list_display = ('name', 'garden',)
    search_fields = ('name', 'garden__name',)


class HarvestAdmin(admin.ModelAdmin):
    fields = ('crop', 'weight', 'plants', 'reportable', 'garden', 'added_by',
              'added', 'updated_by', 'updated',)
    list_display = ('crop', 'weight', 'plants', 'gardener', 'harvested',
                    'reportable',)
    list_filter = ('harvested', 'reportable',)
    readonly_fields = ('added', 'added_by', 'garden', 'updated',)
    search_fields = ('crop__name', 'gardener__name', 'gardener__garden__name',)

    def mark_as_unreportable(self, request, queryset):
        """mark a set of varieties as unreportable"""
        rows = queryset.update(reportable=False)
        if rows == 1:
            bit = "1 harvest"
        else:
            bit = "%s harvests" % rows
        self.message_user(request, "%s marked as unreportable" % bit)

    def mark_as_reportable(self, request, queryset):
        """mark a set of varieties as reportable"""
        rows = queryset.update(reportable=True)
        if rows == 1:
            bit = "1 harvest"
        else:
            bit = "%s harvests" % rows
        self.message_user(request, "%s marked as reportable" % bit)

    actions = (mark_as_unreportable, mark_as_reportable,)


admin.site.register(Gardener, GardenerAdmin)
admin.site.register(Harvest, HarvestAdmin)
