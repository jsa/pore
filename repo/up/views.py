import logging
import re

from google.appengine.api import blobstore
from google.appengine.ext.blobstore.blobstore import BlobInfo

from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.http import urlencode
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
import json


@require_GET
@never_cache
def get_upload_url(request):
    up_url = blobstore.create_upload_url(reverse(blobstore_callback))
    return http.HttpResponse(json.dumps({'url': up_url}), 'text/javascript')

def blobstore_callback(request):
    info = None
    key_match = re.search("blob-key=([^;]+);", request.body)
    if key_match:
        info = BlobInfo.get(key_match.group(1).strip('"'))
    if not info:
        return render(request, "upload.html", {'err': True})

    logging.info("Received file: %r" % ((info.filename, info.content_type, info.size, info.key()),))
    from repo.gallery.views import single
    return http.HttpResponseRedirect("%s?%s" % (reverse(single, args=[1]), urlencode({'ty': ''})))
