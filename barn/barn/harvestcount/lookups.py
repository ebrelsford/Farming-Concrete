from django.db import connection
from django.db.models import Q

from models import Gardener

class GardenerLookup(object):
    """Lookup for Gardeners"""

    def get_query(self, q, request):
        gardeners = Gardener.objects.filter(name__icontains=q)

        try:
            gardeners = gardeners.filter(garden__pk=request.GET['garden'])
        except KeyError:
            return []

        return gardeners

    def format_result(self, gardener):
        return u"%s" % (gardener.name,)

    def format_item(self, gardener):
        return unicode(gardener)

    def get_objects(self,ids):
        """given a list of ids, return the objects ordered as you would like them on the admin page.
        this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return Gardener.objects.filter(pk__in=ids).order_by('name')
