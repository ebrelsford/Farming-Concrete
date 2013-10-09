from django.contrib import admin

from .models import Mood


class MoodAdmin(admin.ModelAdmin):
    fields = ('name', 'type',)
    list_display = ('name', 'type',)


admin.site.register(Mood, MoodAdmin)
