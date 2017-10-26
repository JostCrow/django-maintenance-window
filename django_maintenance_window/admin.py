from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import MaintenanceMode


admin.site.register(MaintenanceMode, SingletonModelAdmin)
