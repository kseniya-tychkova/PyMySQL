from threading import local

from . import err

__comment_storage = local()


def set_comment(comment):
    if comment.find('*/') >= 0 or comment.find('/*') >= 0:
        raise err.ProgrammingError('Wrong comment format')
    __comment_storage.comment = comment


def get_comment():
    return getattr(__comment_storage, 'comment', None)


def with_comment(func):
    def wrapper(self, sql, *args, **kwargs):
        comment = get_comment()
        if comment is not None:
            sql = '/* %s */ %s' % (comment, sql)
        return func(self, sql, *args, **kwargs)
    return wrapper
