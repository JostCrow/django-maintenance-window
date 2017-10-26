from django.conf import settings


MAINTENANCE_TEMPLATE = getattr(
    settings, 'MAINTENANCE_TEMPLATE',
    'django_maintenance_window/maintenance.html'
)

MAINTENANCE_DISPLAY_END_DATE = getattr(
    settings, 'MAINTENANCE_DISPLAY_END_DATE', False
)

MAINTENANCE_EXCLUDE_ADMIN_URLS = getattr(
    settings, 'MAINTENANCE_EXCLUDE_ADMIN_URLS', True
)

MAINTENANCE_EXCLUDE_SUPER_USER = getattr(
    settings, 'MAINTENANCE_EXCLUDE_SUPER_USER', False
)

MAINTENANCE_EXCLUDE_STAFF_USER = getattr(
    settings, 'MAINTENANCE_EXCLUDE_STAFF_USER', False
)
