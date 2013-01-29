from models import Garden, Variety


def is_garden_used(gardenpk):
    garden = Garden.objects.get(pk=gardenpk)
    if garden.gardener_set.all().count() > 0:
        print 'garden has gardeners'
        return True
    if garden.box_set.all().count() > 0:
        print 'garden has boxes'
        return True
    if garden.sharedreport_set.all().count() > 0:
        print 'garden has sharedreports'
        return True
    if garden.chart_set.all().count() > 0:
        print 'garden has chart'
        return True
    if garden.userprofile_set.all().count() > 0:
        print 'garden has users'
        return True

    print 'garden is unused'
    return False


def consolidate_garden(to_delete, to_keep):
    updated = to_delete.gardener_set.all().update(garden=to_keep)
    print 'consolidating gardeners ... %d updated' % updated

    updated = to_delete.box_set.all().update(garden=to_keep)
    print 'consolidating boxes ... %d updated' % updated

    updated = to_delete.sharedreport_set.all().update(garden=to_keep)
    print 'consolidating sharedreports ... %d updated' % updated

    updated = to_delete.chart_set.all().update(garden=to_keep)
    print 'consolidating charts ... %d updated' % updated

    for profile in to_delete.userprofile_set.all():
        profile.gardens.add(to_keep)
        profile.gardens.remove(to_delete)
        print 'consolidating userprofiles'

    print 'copying data fields'
    to_keep.name = to_delete.name
    to_keep.type = to_delete.type
    to_keep.gardenid = to_delete.gardenid
    to_keep.address = to_delete.address
    to_keep.borough = to_delete.borough
    to_keep.neighborhood = to_delete.neighborhood
    to_keep.zip = to_delete.zip
    to_keep.longitude = to_delete.longitude
    to_keep.latitude = to_delete.latitude
    to_keep.save()

    to_delete.delete()
    print 'deleted!'


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
