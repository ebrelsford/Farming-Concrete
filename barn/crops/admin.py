from django.contrib import admin

from estimates.models import EstimatedCost, EstimatedYield
from metrics.cropcount.models import Patch
from metrics.harvestcount.models import Harvest
from metrics.yumyuck.models import YumYuck

from .models import Crop


class CropAdmin(admin.ModelAdmin):
    readonly_fields = ('added', 'updated')
    fields = ('name', 'added_by', 'added', 'updated_by', 'updated',
              'needs_moderation')
    list_display = ('name', 'added_by', 'added', 'needs_moderation')
    list_filter = ('needs_moderation', 'added_by', 'added',)
    search_fields = ('name',)

    def mark_as_moderated(self, request, queryset):
        """mark a set of crops as moderated"""
        rows = queryset.update(needs_moderation=False)
        if rows == 1:
            bit = "1 crop"
        else:
            bit = "%s crops" % rows
        self.message_user(request, "%s marked as moderated" % bit)

    def consolidate(self, request, queryset):
        moderated = queryset.filter(needs_moderation=False)
        if len(moderated) != 1:
            self.message_user(request, ('Not sure which crop to consolidate '
                                        'on. No changes made.'))
            return

        moderated = moderated[0]
        unmoderated = queryset.filter(needs_moderation=True)
        num_consolidated = unmoderated.count()

        EstimatedCost.objects.filter(crop__in=unmoderated).update(crop=moderated)
        EstimatedYield.objects.filter(crop__in=unmoderated).update(crop=moderated)
        Harvest.objects.filter(crop__in=unmoderated).update(crop=moderated)
        Patch.objects.filter(crop__in=unmoderated).update(crop=moderated)
        YumYuck.objects.filter(crop__in=unmoderated).update(crop=moderated)

        unmoderated.delete()
        self.message_user(request, 'Consolidated %d varieties on %s' %
                          (num_consolidated, moderated.name))

    actions = (mark_as_moderated, consolidate)


admin.site.register(Crop, CropAdmin)
