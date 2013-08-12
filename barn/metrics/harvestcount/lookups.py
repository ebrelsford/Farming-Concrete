from .models import Gardener


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
        return Gardener.objects.filter(pk__in=ids).order_by('name')
