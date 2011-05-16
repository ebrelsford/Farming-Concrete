from cropcount.models import Box, Patch
from django.contrib import admin

class BoxInline(admin.TabularInline):
    model = Box
    extra = 1
    fields = ('name', 'length', 'width')

admin.site.register(Patch)
