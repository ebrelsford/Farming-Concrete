from models import Variety

def get_variety(name, user):
    """Get a variety with the given name, creating it if necessary"""
    if not name or not user:
        return None, False

    # try to find an already-existing variety with that name
    varieties = Variety.objects.filter(
        name__istartswith=name, 
        needs_moderation=False
    ) 
    if varieties:
        return varieties[0], False

    # try to find a variety this user added but is not moderated
    user_varieties = Variety.objects.filter(
        name__istartswith=name, 
        added_by=user
    )
    if user_varieties:
        return user_varieties[0], False

    # else create one
    moderated = not user.has_perm('farmingconcrete.add_variety_unmoderated')
    variety = Variety(name=name, added_by=user, needs_moderation=moderated)
    variety.save()
    return variety, True
