# -*- coding: utf-8 -*-

import django
from django.shortcuts import render
from django.utils.cache import add_never_cache_headers

from .models import MaintenanceMode
from .settings import MAINTENANCE_TEMPLATE, MAINTENANCE_DISPLAY_END_DATE

if django.VERSION < (1, 10):
    MaintenanceModeMiddlewareBaseClass = object
else:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    from django.utils.deprecation import MiddlewareMixin
    MaintenanceModeMiddlewareBaseClass = MiddlewareMixin


class MaintenanceModeMiddleware(MaintenanceModeMiddlewareBaseClass):
    """This middleware will check if the maintenance page should be shown."""

    def process_request(self, request):
        """
        This function will check if maintenance is activated.
        If so return the maintenance page.
        Otherwise continue the request.
        """
        config = MaintenanceMode.get_solo()

        if config.maintenance and not request.path.startswith('/admin/'):
            kwargs = {
                'end_date': config.maintenance_until,
                'display_end_date': MAINTENANCE_DISPLAY_END_DATE
            }

            response = render(
                request, MAINTENANCE_TEMPLATE, content_type='text/html', status=503, context=kwargs)
            add_never_cache_headers(response)
            return response
        return None
