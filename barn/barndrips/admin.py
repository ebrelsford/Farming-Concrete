from django.contrib import admin

from drip.admin import DripAdmin

from .models import BarnGardenDrip


admin.site.register(BarnGardenDrip, DripAdmin)
