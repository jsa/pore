from django import http
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from repo.util import render_to


@require_GET
@cache_control(public=True, max_age=4 * 7 * 24 * 60 * 60)
def photo(request, photo_id):
    return http.HttpResponse()

@require_GET
@render_to("gallery.html")
def gallery(request):
    pass
