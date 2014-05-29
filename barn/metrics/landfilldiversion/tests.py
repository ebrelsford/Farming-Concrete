from django.core.urlresolvers import reverse

from ..tests import MetricTest


class LandfillDiversionViewsTest(MetricTest):

    def test_volume_garden_details(self):
        resp = self.client.get(reverse('landfilldiversion_volume_garden_details',
                                       kwargs=self.get_garden_details_kwargs()))
        self.assertEqual(resp.status_code, 200)

    def test_weight_garden_details(self):
        resp = self.client.get(reverse('landfilldiversion_weight_garden_details',
                                       kwargs=self.get_garden_details_kwargs()))
        self.assertEqual(resp.status_code, 200)
