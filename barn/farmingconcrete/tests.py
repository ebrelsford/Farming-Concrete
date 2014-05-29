from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


username = 'eric'
year = 2014


def login(client):
    return client.post(reverse('django.contrib.auth.views.login'), {
        'username': username,
        'password': 'muppet',
    })


def get_user():
    return User.objects.get(username=username)


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
        self.assertEqual(resp.status_code, 200)
