from accounts.models import UserProfile
from farmingconcrete.models import GardenType
from .mobile import is_mobile

def garden_types(request):
    """
    Context processor that provides the GardenTypes available for the given user.
    """
    user = request.user

    if user and user.is_authenticated():
        try:
            profile = user.get_profile()
            types = GardenType.objects.all()
            if profile.garden_types.all().count() > 0:
                types = types & profile.garden_types.all()
            return { 'garden_types': types }
        except UserProfile.DoesNotExist:
            pass
    return {}

def mobile(request):
    """
    Add is_mobile: True if user agent contains an obvious smartphone, False
    otherwise
    """
    return { 'is_mobile': is_mobile(request), }
