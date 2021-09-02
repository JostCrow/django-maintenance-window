# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from recurrence.fields import RecurrenceField
from solo.models import SingletonModel


class MaintenanceMode(SingletonModel):
    maintenance = models.BooleanField(default=False)
    maintenance_from = models.DateTimeField(null=True, blank=True)
    maintenance_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return u"Maintenance Mode"

    class Meta:
        verbose_name = _("Maintenance Mode")

    def clean(self):
        error_message = _('You can not set "maintenance_from" without setting "maintenance_until"')  # noqa
        if self.maintenance_from and not self.maintenance_until:
            raise ValidationError(error_message)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Schedule(models.Model):
    mode = models.ForeignKey(MaintenanceMode, on_delete=models.CASCADE, related_name="schedules")
    recurrences = RecurrenceField()
    start_time = models.TimeField(null=True, blank=True)
    stop_time = models.TimeField(null=True, blank=True)

    def clean(self):
        error_message = _('You can not set "start_time" without setting "stop_time"')
        if self.start_time and not self.stop_time:
            raise ValidationError(error_message)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
