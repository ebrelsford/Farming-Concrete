from django.core.urlresolvers import reverse

from ..tests import MetricTest


class LookingGoodViewsTest(MetricTest):

    def test_garden_details(self):
        resp = self.client.get(reverse('lookinggood_event_garden_details',
                                       kwargs=self.get_garden_details_kwargs()))
        self.assertEqual(resp.status_code, 200)
