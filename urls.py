from django import http
from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

from repo.gallery import views as gallery
from repo.up import views as up

# default error handlers
from django.conf.urls.defaults import handler404, handler500


urlpatterns = patterns('',
    url(r"^i/(\d+)-(\d+)(-.+)?.jpg", gallery.photo, name="entry.photo"),
    url(r"^$", gallery.browse, name="gallery.browse"),
    url(r"^(\d+)/$", gallery.single, name="gallery.entry"),
    url(r"^about/$", direct_to_template, {'template': "about.html"}, name="about"),
    url(r"^upload/$", direct_to_template, {'template': "upload.html"}, name="upload"),
    url(r"^upload-url/$", up.get_upload_url, name="upload.url"),
    (r"^_ah/blobstore-callback/$", up.blobstore_callback),
    (r"^_ah/warmup/$", lambda *a, **kw: http.HttpResponse()),
)
