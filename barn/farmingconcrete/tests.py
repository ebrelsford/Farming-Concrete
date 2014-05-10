from django.core.urlresolvers import reverse
from django.test import TestCase


def login(client):
    return client.post(reverse('django.contrib.auth.views.login'), {
        'username': 'eric',
        'password': 'muppet',
    })


class FarmingConcreteViewsTest(TestCase):
    fixtures = ['farmingconcrete_test.json', 'accounts_test.json',]

    def test_index(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        self.client.get(reverse('home'))
        resp = login(self.client)
        self.assertEqual(resp.status_code, 302)

    def test_gardens(self):
        login(self.client)
        resp = self.client.get(reverse('farmingconcrete_gardens_user'))
        print resp.content
        self.assertEqual(resp.status_code, 200)
