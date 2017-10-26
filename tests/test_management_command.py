from datetime import timedelta

from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from django_maintenance_window.models import MaintenanceMode


class MiddleWareTests(TestCase):
    def test_call_command(self):
        call_command('check_maintenance_mode')

        config = MaintenanceMode.get_solo()
        self.assertFalse(config.maintenance)

    def test_call_command_with_from_and_until(self):
        config = MaintenanceMode.get_solo()
        config.maintenance_from = timezone.now() - timedelta(minutes=5)
        config.maintenance_until = timezone.now()
        config.save()
        call_command('check_maintenance_mode')

        config = MaintenanceMode.get_solo()
        self.assertTrue(config.maintenance)

    def test_call_command_with_from_future_and_until(self):
        config = MaintenanceMode.get_solo()
        config.maintenance_from = timezone.now() + timedelta(minutes=5)
        config.maintenance_until = timezone.now()
        config.save()
        call_command('check_maintenance_mode')

        config = MaintenanceMode.get_solo()
        self.assertFalse(config.maintenance)

    def test_call_command_with_until_and_active(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.maintenance_until = timezone.now() - timedelta(minutes=5)
        config.save()
        call_command('check_maintenance_mode')

        config = MaintenanceMode.get_solo()
        self.assertFalse(config.maintenance)

    def test_call_command_with_until_future_and_active(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.maintenance_until = timezone.now() + timedelta(minutes=5)
        config.save()
        call_command('check_maintenance_mode')

        config = MaintenanceMode.get_solo()
        self.assertTrue(config.maintenance)
