from farmingconcrete.models import Garden


class GardenLookup(object):
    """Lookup for Gardens"""

    def get_query(self, q, request):
        gardens = Garden.objects.filter(name__icontains=q)

        try:
            # get type field extraParam
            selected_type = request.GET['type']
            gardens = gardens.filter(type=selected_type)
        except KeyError:
            pass

        return gardens

    def format_result(self, garden):
        return u"%s (%s)" % (garden.name, garden.borough)

    def format_item(self, garden):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return unicode(garden)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
        this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return Garden.objects.filter(pk__in=ids).order_by('name')
