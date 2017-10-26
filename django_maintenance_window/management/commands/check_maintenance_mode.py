from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Enable/Disabled Maintenance Mode if time is passed"

    def handle(self, *args, **options):
        from django_maintenance_window.models import MaintenanceMode
        config = MaintenanceMode.get_solo()
        now = timezone.now()

        if config.maintenance:
            if config.maintenance_until < now:
                config.maintenance = False
                config.maintenance_until = None
                config.save()
        else:
            if config.maintenance_from and config.maintenance_from < now:
                config.maintenance = True
                config.maintenance_from = None
                config.save()
