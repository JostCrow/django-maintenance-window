from __future__ import absolute_import, unicode_literals

from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/2fa", TemplateView.as_view(template_name='base.html'), name="two-factor"),
    path("", TemplateView.as_view(template_name='base.html'), name='home'),
]
