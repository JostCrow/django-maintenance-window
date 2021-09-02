from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import MaintenanceMode, Schedule


class ScheduleInlineAdmin(admin.TabularInline):
    model = Schedule
    extra = 1


@admin.register(MaintenanceMode)
class MaintenanceModeAdmin(SingletonModelAdmin):
    inlines = [ScheduleInlineAdmin]
