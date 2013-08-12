from django.contrib import admin

from estimates.models import EstimatedCost, EstimatedYield
from metrics.cropcount.admin import BoxInline
from metrics.cropcount.models import Patch
from metrics.harvestcount.models import Harvest
from .models import Garden, GardenGroup, GardenType, Variety


class GardenAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'neighborhood', 'borough', 'city', 'state',)
    list_filter = ('type', 'borough', 'neighborhood', 'state',)
    search_fields = ('name', 'neighborhood', 'borough',)
    inlines = (BoxInline,)


class VarietyAdmin(admin.ModelAdmin):
    readonly_fields = ('added', 'updated')
    fields = ('name', 'added_by', 'added', 'updated_by', 'updated',
              'needs_moderation')
    list_display = ('name', 'added_by', 'added', 'needs_moderation')
    list_filter = ('needs_moderation', 'added_by', 'added',)
    search_fields = ('name',)

    def mark_as_moderated(self, request, queryset):
        """mark a set of varieties as moderated"""
        rows = queryset.update(needs_moderation=False)
        if rows == 1:
            bit = "1 variety"
        else:
            bit = "%s varieties" % rows
        self.message_user(request, "%s marked as moderated" % bit)

    def consolidate(self, request, queryset):
        moderated = queryset.filter(needs_moderation=False)
        if len(moderated) != 1:
            self.message_user(request, ('Not sure which variety to consolidate'
                                        'on. No changes made.'))
            return

        moderated = moderated[0]
        unmoderated = queryset.filter(needs_moderation=True)
        num_consolidated = unmoderated.count()

        Patch.objects.filter(variety__in=unmoderated).update(variety=moderated)
        Harvest.objects.filter(variety__in=unmoderated).update(variety=moderated)
        EstimatedCost.objects.filter(
            variety__in=unmoderated
        ).update(variety=moderated)
        EstimatedYield.objects.filter(
            variety__in=unmoderated
        ).update(variety=moderated)
        unmoderated.delete()
        self.message_user(request, 'Consolidated %d varieties on %s' %
                          (num_consolidated, moderated.name))

    actions = (mark_as_moderated, consolidate)


admin.site.register(Garden, GardenAdmin)
admin.site.register(GardenGroup)
admin.site.register(GardenType)
admin.site.register(Variety, VarietyAdmin)
