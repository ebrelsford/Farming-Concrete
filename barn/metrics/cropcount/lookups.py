from farmingconcrete.models import Garden


class UncountedGardenLookup(object):
    """Lookup for Gardens that have not yet been included in Crop Count"""

    def get_query(self, q, request):
        gardens = Garden.objects.filter(name__icontains=q)

        try:
            # get type field extraParam
            selected_type = request.GET['type']
            gardens = gardens.filter(type=selected_type)
        except:
            pass

        return gardens

    def format_result(self, garden):
        return u"%s (%s)" % (garden.name, garden.borough)

    def format_item(self, garden):
        """
        The display of a currently selected object in the area below the
        search box. Html is OK
        """
        return unicode(garden)

    def get_objects(self,ids):
        """
        Given a list of ids, return the objects ordered as you would like them
        on the admin page. This is for displaying the currently selected items
        (in the case of a ManyToMany field).
        """
        return Garden.objects.filter(pk__in=ids).order_by('name')

