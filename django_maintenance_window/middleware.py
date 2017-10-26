# -*- coding: utf-8 -*-

import django
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.cache import add_never_cache_headers

from . import settings
from .models import MaintenanceMode

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

        admin_root_url = reverse('admin:index')

        skip_maintenance = False
        if request.path.startswith(admin_root_url) and settings.MAINTENANCE_EXCLUDE_ADMIN_URLS:
            skip_maintenance = True
        if request.user.is_superuser and settings.MAINTENANCE_EXCLUDE_SUPER_USER:
            skip_maintenance = True
        if request.user.is_staff and settings.MAINTENANCE_EXCLUDE_STAFF_USER:
            skip_maintenance = True

        if config.maintenance and not skip_maintenance:
            kwargs = {
                'end_date': config.maintenance_until,
                'display_end_date': settings.MAINTENANCE_DISPLAY_END_DATE
            }

            response = render(
                request, settings.MAINTENANCE_TEMPLATE,
                content_type='text/html', status=503, context=kwargs)
            add_never_cache_headers(response)
            return response
        return None
