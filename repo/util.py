from django import http
from django.template.context import RequestContext
from django.template.loader import get_template


def render_to(template):
    def decorator(fn):
        def wrapper(request, *args, **kwargs):
            ctx = fn(request, *args, **kwargs)
            if isinstance(ctx, http.HttpResponse):
                return ctx
            return http.HttpResponse(get_template(template).render(RequestContext(request, ctx)))
        return wrapper
    return decorator
