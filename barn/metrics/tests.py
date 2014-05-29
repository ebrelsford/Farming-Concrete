from django.test import TestCase

from farmingconcrete.tests import get_user, login, year


class MetricTest(TestCase):
    fixtures = ['farmingconcrete_test.json', 'accounts_test.json',]

    def setUp(self):
        login(self.client)
        self.user = get_user()
        self.garden = self.user.get_profile().gardens.all()[0]

    def get_garden_details_kwargs(self):
        return {
            'pk': self.garden.pk,
            'year': year
        }
