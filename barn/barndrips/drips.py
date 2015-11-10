from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.template import Context
from django.utils.timezone import now

from drip.drips import DripBase, DripMessage

from accounts.models import GardenMembership
from farmingconcrete.models import Garden


class BarnGardenDripBase(DripBase):
    def queryset(self):
        """
        Select Users where the number of gardens added by that user is one.
        """
        gardens = Garden.objects.values('added_by') \
                .annotate(count=Count('id')).filter(count=1)
        single_garden_users = [g['added_by'] for g in gardens]
        users = get_user_model().objects.filter(
            date_joined__gte=now() - timedelta(days=14),
            pk__in=single_garden_users
        )
        return users


class GardenMessage(DripMessage):
    """Override default DripMessage and add user's garden to context."""

    @property
    def context(self):
        context = super(GardenMessage, self).context
        if not context:
            context = Context({'user': self.user})
        context['garden'] = Garden.objects.filter(added_by=self.user)[0]
        self._context = context
        return context


class HundredRecordMessage(DripMessage):
    """
    Override default DripMessage and add user's 100-record garden to 
    context.
    """

    @property
    def context(self):
        context = super(HundredRecordMessage, self).context
        if not context:
            context = Context({'user': self.user})
        context['garden'] = Garden.objects.filter(
            gardenmembership__is_admin=True,
            gardenmembership__user_profile__user=self.user,
            metric_record_added__gte=now() - timedelta(days=2),
            metric_records_count__gte=100,
        )[0]
        self._context = context
        return context


class HundredRecordDripBase(DripBase):
    def queryset(self):
        """
        Select users that are admins of gardens with over 100 records and have
        added records in the past few days.
        """
        garden_memberships = GardenMembership.objects.filter(
            garden__metric_record_added__gte=now() - timedelta(days=2),
            garden__metric_records_count__gte=100,
            is_admin=True,
        )
        users = get_user_model().objects.filter(
            userprofile__gardenmembership__in=garden_memberships,
        )
        return users
