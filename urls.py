from django import http
from django.conf.urls import patterns

from repo.gallery import views as gallery

# default error handlers
from django.conf.urls.defaults import handler404, handler500


urlpatterns = patterns('',
    (r"^i/(\d+).jpg", gallery.photo),
    (r"^$", gallery.gallery),
    (r"^_ah/warmup/$", lambda *a, **kw: http.HttpResponse()),
)
