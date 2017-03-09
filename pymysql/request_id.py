import sys
from threading import local

__request_id_storage = local()


def set_request_id(request_id):
    __request_id_storage.request_id = request_id


def get_request_id():
    return getattr(__request_id_storage, 'request_id', None)


def with_request_id(func):
    def wrapper(self, sql, *args, **kwargs):
        request_id = get_request_id()
        if not request_id:
            request_id = " ".join(sys.argv)

        comment = "/* request_id: %s */" % request_id

        return func(self, comment + sql, *args, **kwargs)
    return wrapper
