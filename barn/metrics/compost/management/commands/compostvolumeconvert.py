from django.core.management.base import BaseCommand

from pint import UnitRegistry

from ...models import CompostProductionVolume

ureg = UnitRegistry()


class Command(BaseCommand):
    help = 'Convert old-style compost volumes to new-style'

    def handle(self, *args, **options):
        records = CompostProductionVolume.objects.filter(
            volume__isnull=False,
            volume_new__isnull=True
        )
        for record in records:
            # volume is currently in gallons, fix that
            cubic_centimeters = (record.volume * ureg.gallon).to(ureg.cubic_centimeter).magnitude
            record.volume_new = cubic_centimeters / (100 ** 3)
            record.save()
