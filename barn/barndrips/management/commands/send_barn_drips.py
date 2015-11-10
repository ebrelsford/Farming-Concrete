from django.core.management.base import BaseCommand

from barndrips.models import BarnGardenDrip


class Command(BaseCommand):
    def handle(self, *args, **options):
        for drip in BarnGardenDrip.objects.filter(enabled=True):
            sent = drip.drip.run()
            print 'Sent %d messages for drip "%s"' % (sent, drip)
