from django.contrib import admin

from drip.admin import DripAdmin

from .models import (BarnGardenDrip, BarnHundredRecordDrip,
                     BarnInactiveGardenDrip)


admin.site.register(BarnGardenDrip, DripAdmin)
admin.site.register(BarnHundredRecordDrip, DripAdmin)
admin.site.register(BarnInactiveGardenDrip, DripAdmin)
