=============================
django-maintenance-window
=============================

.. image:: https://badge.fury.io/py/django-maintenance-window.svg
    :target: https://badge.fury.io/py/django-maintenance-window

.. image:: https://travis-ci.org/JostCrow/django-maintenance-window.svg?branch=master
    :target: https://travis-ci.org/JostCrow/django-maintenance-window

.. image:: https://codecov.io/gh/JostCrow/django-maintenance-window/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/JostCrow/django-maintenance-window

.. image:: https://lintly.com/gh/JostCrow/django-maintenance-window/badge.svg
    :target: https://lintly.com/gh/JostCrow/django-maintenance-window/
    :alt: Lintly

.. image:: https://bettercodehub.com/edge/badge/JostCrow/django-maintenance-window?branch=master
    :target: https://bettercodehub.com/results/JostCrow/django-maintenance-window

.. image:: https://api.codeclimate.com/v1/badges/6583656ee5ab17179caf/maintainability
   :target: https://codeclimate.com/github/JostCrow/django-maintenance-window/maintainability
   :alt: Maintainability

Your project description goes here

Documentation
-------------

The full documentation is at https://django-maintenance-window.readthedocs.io.

Quickstart
----------

Install django-maintenance-window::

    pip install django-maintenance-window

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django-solo',
        'django_maintenance_window',
        ...
    )

Add django-maintenance-window's middleware to the middleware:

.. code-block:: python


    MIDDLEWARE_CLASSES = [
        ...
        'django_maintenance_window.middleware.MaintenanceModeMiddleware',
        ...
    ]

or

.. code-block:: python


    MIDDLEWARE = [
        ...
        'django_maintenance_window.middleware.MaintenanceModeMiddleware',
        ...
    ]

Settings
--------

* MAINTENANCE_TEMPLATE = 'django_maintenance_window/maintenance.html'
    Overwrite the template that is used for the maintenance template
* MAINTENANCE_DISPLAY_END_DATE = False
    If the end date should be displayed at the bottom of the page.
* MAINTENANCE_EXCLUDE_ADMIN_URLS = True
    This will allow accessing the admin even if maintenance mode is active.
* MAINTENANCE_EXCLUDE_SUPER_USER = False
    This will allow super users to see the site even if maintenance mode is active.
* MAINTENANCE_EXCLUDE_STAFF_USER = False
    This will allow staff users to see the site even if maintenance mode is active.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
