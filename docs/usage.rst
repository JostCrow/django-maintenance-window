=====
Usage
=====

To use django-maintenance-window in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_maintenance_window.apps.DjangoMaintenanceWindowConfig',
        ...
    )

Add django-maintenance-window's URL patterns:

.. code-block:: python

    from django_maintenance_window import urls as django_maintenance_window_urls


    urlpatterns = [
        ...
        url(r'^', include(django_maintenance_window_urls)),
        ...
    ]
