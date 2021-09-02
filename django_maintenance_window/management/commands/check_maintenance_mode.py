import logging
import pytz
import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Enable/Disabled Maintenance Mode if time is passed"

    def handle(self, *args, **options):
        from django_maintenance_window.models import MaintenanceMode
        config = MaintenanceMode.get_solo()
        unaware_now = datetime.now()
        now = pytz.timezone("Europe/Amsterdam").localize(unaware_now)
        if config.maintenance:
            logger.info("Try disabling maintenance mode")
            self.disable_maintenance_mode(config, now)
        else:
            logger.info("Try enabling maintenance mode")
            self.enable_maintenance_mode(config, now)

    def datetime_from_utc_to_local(self, utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset

    def enable_maintenance_mode(self, config, now):
        if config.maintenance_from and config.maintenance_from < now:
            logger.info("Maintenance from found.")
            logger.info("Enable maintenance mode.")
            config.maintenance = True
            config.maintenance_from = None
            config.save()
            return

        for schedule in config.schedules.all():
            unaware = datetime.now() - timedelta(days=1)
            later = datetime.now() + timedelta(days=1)
            between = schedule.recurrences.between(unaware, later, inc=True)
            if between:
                scheduled_date = between[0]
                start = pytz.timezone("Europe/Amsterdam").localize(datetime(
                    year=scheduled_date.year,
                    month=scheduled_date.month,
                    day=scheduled_date.day,
                    hour=schedule.start_time.hour,
                    minute=schedule.start_time.minute,
                    second=schedule.start_time.second,
                ))
                end = pytz.timezone("Europe/Amsterdam").localize(datetime(
                    year=scheduled_date.year,
                    month=scheduled_date.month,
                    day=scheduled_date.day,
                    hour=schedule.stop_time.hour,
                    minute=schedule.stop_time.minute,
                    second=schedule.stop_time.second,
                ))
                if start < now and now < end:
                    logger.info("Enable maintenance mode. (via schedule)")
                    config.maintenance = True
                    config.save()
                    return

    def disable_maintenance_mode(self, config, now):
        if config.maintenance_until and config.maintenance_until < now:
            logger.info("Maintenance until found.")
            logger.info("Disable maintenance mode.")
            config.maintenance = False
            config.maintenance_until = None
            config.save()
            return

        for schedule in config.schedules.all():
            unaware = datetime.now() - timedelta(days=1)
            later = datetime.now() + timedelta(days=1)
            between = schedule.recurrences.between(unaware, later, inc=True)
            if between:
                scheduled_date = between[0]
                end = pytz.timezone("Europe/Amsterdam").localize(datetime(
                    year=scheduled_date.year,
                    month=scheduled_date.month,
                    day=scheduled_date.day,
                    hour=schedule.stop_time.hour,
                    minute=schedule.stop_time.minute,
                    second=schedule.stop_time.second,
                ))

                if end < now:
                    logger.info("Disable maintenance mode. (via schedule)")
                    config.maintenance = False
                    config.save()
                    return
