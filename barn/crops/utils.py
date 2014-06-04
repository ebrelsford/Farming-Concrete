from .models import Crop


def get_crop(name, user):
    """Get a crop with the given name, creating it if necessary"""
    if not name or not user:
        return None, False

    # Try to find an already-existing crop with that name
    crops = Crop.objects.filter(
        name__istartswith=name,
        needs_moderation=False
    )
    if crops:
        return crops[0], False

    # Try to find a crop this user added but is not moderated
    user_crops = Crop.objects.filter(name__istartswith=name, added_by=user)
    if user_crops:
        return user_crops[0], False

    # Else create one
    moderated = not user.has_perm('crops.add_crop_unmoderated')
    crop = Crop(name=name, added_by=user, needs_moderation=moderated)
    crop.save()
    return crop, True
