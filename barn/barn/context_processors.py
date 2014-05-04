from accounts.utils import get_profile
from farmingconcrete.models import GardenType
from .mobile import is_mobile

def garden_types(request):
    """
    Context processor that provides the GardenTypes available for the given user.
    """
    user = request.user

    if user and user.is_authenticated():
        profile = get_profile(user)
        types = GardenType.objects.all()
        if profile.garden_types.all().count() > 0:
            types = types & profile.garden_types.all()
        return { 'garden_types': types }
    return {}

def mobile(request):
    """
    Add is_mobile: True if user agent contains an obvious smartphone, False
    otherwise
    """
    return { 'is_mobile': is_mobile(request), }
