from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django_maintenance_window.models import MaintenanceMode

User = get_user_model()


class MiddleWareTests(TestCase):
    def setUp(self):
        self.url = reverse("home")

        self.user = User.objects.create_user(
            username="normal user",
            email="email",
            password="password",
            is_staff=False,
            is_superuser=False,
        )
        self.staff = User.objects.create_user(
            username="Staff user",
            email="email",
            password="password",
            is_staff=True,
            is_superuser=False,
        )
        self.superuser = User.objects.create_user(
            username="Super user",
            email="email",
            password="password",
            is_staff=True,
            is_superuser=True,
        )

    def test_normal_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_maintenance_view(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 503)

    @override_settings(MAINTENANCE_EXCLUDE_SUPER_USER=True)
    def test_exclude_super_user(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.save()

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 503)

        self.client.force_login(self.staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 503)

        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @override_settings(MAINTENANCE_EXCLUDE_STAFF_USER=True)
    def test_exclude_staff_user(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.save()

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 503)

        self.client.force_login(self.staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @override_settings(MAINTENANCE_EXCLUDE_ADMIN_URLS=True)
    def test_exclude_admin_urls_true(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.save()

        self.client.force_login(self.superuser)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 503)

        admin_url = reverse("admin:index")
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 200)

    @override_settings(MAINTENANCE_EXCLUDE_ADMIN_URLS=False)
    def test_exclude_admin_urls_false(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.save()

        self.client.force_login(self.superuser)

        admin_url = reverse("admin:index")
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 503)

    @override_settings(MAINTENANCE_EXCLUDE_URLS=["/accounts"])
    def test_excluded_urls(self):
        config = MaintenanceMode.get_solo()
        config.maintenance = True
        config.save()

        self.client.force_login(self.superuser)

        url = reverse("two-factor")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
