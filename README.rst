=============================
django-currentdistrict
=============================

----

.. contents:: Conveniently store reference to request district on thread/db level.

----

Quickstart
----------

Install django-currentdistrict::

    pip install django-currentdistrict

Add it to the middleware classes in your settings.py::

    MIDDLEWARE = (
        ...,
        'django_currentdistrict.middleware.ThreadLocalDistrictMiddleware',
    )

Then use it in a project::

    from django_currentdistrict.middleware import (
        get_current_district, get_current_authenticated_district)

    # As model field:
    from django_currentdistrict.db.models import CurrentDistrictField
    class Foo(models.Model):
        created_by = CurrentDistrictField()
