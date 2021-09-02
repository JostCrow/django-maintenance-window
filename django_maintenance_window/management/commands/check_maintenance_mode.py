import pytz

from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Enable/Disabled Maintenance Mode if time is passed"

    def handle(self, *args, **options):
        from django_maintenance_window.models import MaintenanceMode
        config = MaintenanceMode.get_solo()
        now = timezone.now()

        if config.maintenance:
            self.disable_maintenace_mode(config, now)
        else:
            self.enable_maintenace_mode(config, now)

    def enable_maintenace_mode(self, config, now):
        if config.maintenance_from and config.maintenance_from < now:
            config.maintenance = True
            config.maintenance_from = None
            config.save()
            # We do not need to check any further. The maintenace should be enabled.
            return

        for schedule in config.schedules.all():
            unaware = datetime.now().replace(hour=schedule.start_time.hour, minute=schedule.start_time.minute, second=schedule.start_time.second, microsecond=0)
            later = datetime.now().replace(hour=schedule.stop_time.hour, minute=schedule.stop_time.minute, second=schedule.stop_time.second, microsecond=0)
            between = schedule.recurrences.between(unaware, later)
            if between:
                scheduled_date = between[0]
                start = datetime(
                    year=scheduled_date.year,
                    month=scheduled_date.month,
                    day=scheduled_date.day,
                    hour=schedule.start_time.hour,
                    minute=schedule.start_time.minute,
                    second=schedule.start_time.second,
                    tzinfo=pytz.UTC
                )
                if start < now:
                    config.maintenance = True
                    config.save()
                    return

    def disable_maintenace_mode(self, config, now):
        if config.maintenance_until and config.maintenance_until < now:
            config.maintenance = False
            config.maintenance_until = None
            config.save()
            # We do not need to check any further. The maintenace should be disabled.
            return

        for schedule in config.schedules.all():
            unaware = datetime.now().replace(hour=schedule.start_time.hour, minute=schedule.start_time.minute, second=schedule.start_time.second, microsecond=0)
            later = datetime.now().replace(hour=schedule.stop_time.hour, minute=schedule.stop_time.minute, second=schedule.stop_time.second, microsecond=0)
            between = schedule.recurrences.between(unaware, later)
            if between:
                scheduled_date = between[0]
                end = datetime(
                    year=scheduled_date.year,
                    month=scheduled_date.month,
                    day=scheduled_date.day,
                    hour=schedule.stop_time.hour,
                    minute=schedule.stop_time.minute,
                    second=schedule.stop_time.second,
                )
                if end < now:
                    config.maintenance = True
                    config.save()
                    return
