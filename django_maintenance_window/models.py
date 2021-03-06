# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


@python_2_unicode_compatible
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
        return super(MaintenanceMode, self).save(*args, **kwargs)
