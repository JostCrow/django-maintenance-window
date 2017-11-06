#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-maintenance-window
------------

Tests for `django-maintenance-window` models module.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django_maintenance_window import models


class TestDjango_maintenance_window(TestCase):

    def setUp(self):
        pass

    def test_str(self):
        maintenance = models.MaintenanceMode()
        self.assertEqual(str(maintenance), _("Maintenance Mode"))

    def test_from_can_not_be_saved_without_until(self):
        maintenance = models.MaintenanceMode(maintenance_from=timezone.now())
        with self.assertRaises(ValidationError) as exc_context:
            maintenance.save()
        # assert False, exc_context.exception.messages
        self.assertEqual(
            exc_context.exception.messages,
            [_('You can not set "maintenance_from" without setting "maintenance_until"')]  # noqa
        )

    def test_can_be_saved_empty(self):
        maintenance = models.MaintenanceMode()
        maintenance.save()

    def test_can_be_saved_filled(self):
        maintenance = models.MaintenanceMode(
            maintenance=True,
            maintenance_from=timezone.now(),
            maintenance_until=timezone.now()
        )
        maintenance.save()

    def tearDown(self):
        pass
