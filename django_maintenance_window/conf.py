from django.conf import settings as django_settings


class Settings:

    @property
    def MAINTENANCE_TEMPLATE(self):
        return getattr(
            django_settings,
            "MAINTENANCE_TEMPLATE",
            "django_maintenance_window/maintenance.html",
        )

    @property
    def MAINTENANCE_DISPLAY_END_DATE(self):
        return getattr(django_settings, "MAINTENANCE_DISPLAY_END_DATE", False)

    @property
    def MAINTENANCE_EXCLUDE_ADMIN_URLS(self):
        return getattr(django_settings, "MAINTENANCE_EXCLUDE_ADMIN_URLS", True)

    @property
    def MAINTENANCE_EXCLUDE_SUPER_USER(self):
        return getattr(django_settings, "MAINTENANCE_EXCLUDE_SUPER_USER", False)

    @property
    def MAINTENANCE_EXCLUDE_STAFF_USER(self):
        return getattr(django_settings, "MAINTENANCE_EXCLUDE_STAFF_USER", False)

    @property
    def MAINTENANCE_EXCLUDE_URLS(self):
        return getattr(django_settings, "MAINTENANCE_EXCLUDE_URLS", [])


settings = Settings()
