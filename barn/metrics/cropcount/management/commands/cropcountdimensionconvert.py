from django.core.management.base import BaseCommand

from pint import UnitRegistry

from ...models import Box

ureg = UnitRegistry()


class Command(BaseCommand):
    help = 'Convert old-style cropcount bed dimenions to new-style'

    def handle(self, *args, **options):
        beds = Box.objects.filter(
            length__isnull=False,
            length_new__isnull=True,
            width__isnull=False,
            width_new__isnull=True,
        )
        for bed in beds:
            # volume is currently in feet, fix that
            bed.length_new = (bed.length * ureg.foot).to(ureg.meter).magnitude
            bed.width_new = (bed.width * ureg.foot).to(ureg.meter).magnitude
            bed.save()
