from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from ..views import photo, single


register = template.Library()

@register.filter
def og_image(entry):
    return "http://%s%s" % (settings.PRIMARY_HOST,
                            reverse(photo, args=[entry.key.id(), 0, "-300"]))

@register.filter
def og_title(entry):
    return "%s @ %s" % (entry.datestamp or "some time",
                        entry.location or "some place")

@register.filter
def og_url(entry):
    return "http://%s%s" % (settings.PRIMARY_HOST,
                            reverse(single, args=[entry.key.id()]))
