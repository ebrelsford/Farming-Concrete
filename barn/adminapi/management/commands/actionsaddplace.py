from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from actstream.models import Action


class Command(BaseCommand):
    help = 'Populate place field for all existing actions'

    def get_action_object_coordinates(self, action):
        if not action.action_object:
            return None

        try:
            coordinates = [
                action.action_object.longitude,
                action.action_object.latitude,
            ]
            if coordinates[0] and coordinates[1]:
                return coordinates
        except AttributeError:
            pass
        return None

    def get_target_coordinates(self, action):
        if not action.target:
            return None

        try:
            coordinates = [
                action.target.longitude,
                action.target.latitude,
            ]
            if coordinates[0] and coordinates[1]:
                return coordinates
        except AttributeError:
            pass
        return None

    def handle(self, *args, **options):
        for action in Action.objects.all():
            coordinates = self.get_action_object_coordinates(action)
            if not coordinates:
                coordinates = self.get_target_coordinates(action)
            if not coordinates:
                continue
            action.place = Point(coordinates)
            action.save()
