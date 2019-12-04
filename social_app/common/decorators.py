from functools import wraps

from django.http import HttpResponseBadRequest


# Django 2.1+
def ajax_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    return wrap
