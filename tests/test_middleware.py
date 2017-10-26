from django.test import TestCase
from django.core.urlresolvers import reverse
from django_maintenance_window.models import MaintenanceMode


class MiddleWareTests(TestCase):
    def setUp(self):
        self.url = reverse('home')

    def test_normal_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_maintenance_view(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 503)
