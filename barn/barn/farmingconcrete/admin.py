from django.contrib import admin

from models import Garden, GardenType, Variety
from cropcount.admin import BoxInline

class GardenAdmin(admin.ModelAdmin):
    #fields = ('name', 'address', 'neighborhood', 'borough', 'zip', 'gardenid',)
    list_display = ('name', 'neighborhood', 'borough',)
    search_fields = ('name', 'neighborhood', 'borough',)
    inlines = (BoxInline,)

class VarietyAdmin(admin.ModelAdmin):
    readonly_fields = ('added', 'updated')
    fields = ('name', 'added_by', 'added', 'updated_by', 'updated', 'needs_moderation')
    list_display = ('name', 'added_by', 'added', 'needs_moderation')
    list_filter = ('needs_moderation', 'added_by', 'added',)
    actions = ('mark_as_moderated',)

    def mark_as_moderated(self, request, queryset):
        """mark a set of varieties as moderated"""
        rows = queryset.update(needs_moderation=False)
        if rows == 1:
            bit = "1 variety"
        else:
            bit = "%s varieties" % rows
        self.message_user(request, "%s marked as moderated" % bit) 

admin.site.register(Garden, GardenAdmin)
admin.site.register(GardenType)
admin.site.register(Variety, VarietyAdmin)
