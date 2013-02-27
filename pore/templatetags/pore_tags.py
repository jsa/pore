import logging
from urlparse import urlparse

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json


register = template.Library()

def dumps(obj, **kwargs):
    kwargs.setdefault('separators', (',', ':'))
    kwargs.setdefault('cls', DjangoJSONEncoder)
#    kwargs.setdefault('default', custom_encodes)
    return json.dumps(obj, **kwargs)

@register.filter
def js(value):
    try:
        return mark_safe(dumps(value))
    except TypeError, e:
        logging.warning(e, exc_info=1)
        return 'null'
js.is_safe = True

@register.filter
def domain(url):
    urlp = urlparse(url)
    if urlp.netloc:
        domain = urlp.netloc.split(":")[0]
        if "." in domain:
            return ".".join(domain.split(".")[-2:])
        return domain
    return ""
