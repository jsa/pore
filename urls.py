from django import http
from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

from repo.gallery import views as gallery

# default error handlers
from django.conf.urls.defaults import handler404, handler500


urlpatterns = patterns('',
    (r"^i/(\d+).jpg", gallery.photo),
    url(r"^$", gallery.gallery, name="gallery"),
    url(r"^about/$", direct_to_template, {'template': "about.html"}),
    url(r"^upload/$", direct_to_template, {'template': "upload.html"}, name="upload"),
    (r"^_ah/warmup/$", lambda *a, **kw: http.HttpResponse()),
)
