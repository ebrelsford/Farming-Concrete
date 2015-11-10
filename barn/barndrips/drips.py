from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.template import Context
from django.utils.timezone import now

from drip.drips import DripBase, DripMessage

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
