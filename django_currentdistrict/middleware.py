from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from threading import local

DISTRICT_ATTR_NAME = getattr(settings, 'LOCAL_DISTRICT_ATTR_NAME', '_current_district')

_thread_locals = local()


def _do_set_current_district(district_fun):
    setattr(_thread_locals, DISTRICT_ATTR_NAME, district_fun.__get__(district_fun, local))


def _set_current_district(district=None):
    '''
    Sets current district in local thread.

    Can be used as a hook e.g. for shell jobs (when request object is not
    available).
    '''
    _do_set_current_district(lambda self: district)


class ThreadLocalDistrictMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.district_context closure; asserts laziness;
        # memorization is implemented in
        # request.district_context (non-data descriptor)
        _do_set_current_district(lambda self: getattr(request, 'district_context', None))
        response = self.get_response(request)
        return response


def get_current_district():
    current_district = getattr(_thread_locals, DISTRICT_ATTR_NAME, None)
    if callable(current_district):
        return current_district()
    return current_district


def get_current_verified_district():
    current_district = get_current_district()
    if current_district is None:
        return None
    return current_district
