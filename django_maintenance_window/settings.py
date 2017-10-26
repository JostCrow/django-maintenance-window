from django.conf import settings


MAINTENANCE_TEMPLATE = getattr(
    settings, 'MAINTENANCE_TEMPLATE',
    'django_maintenance_window/maintenance.html'
)

MAINTENANCE_DISPLAY_END_DATE = getattr(
    settings, 'MAINTENANCE_DISPLAY_END_DATE', False
)
