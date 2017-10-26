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

    def save(self, *args, **kwargs):
        if self.maintenance_from and not self.maintenance_until:
            raise ValidationError(_('You can not set "maintenance_from" without setting "maintenance_until"'))
        super(MaintenanceMode, self).save(*args, **kwargs)
