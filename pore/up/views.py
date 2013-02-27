from datetime import datetime
import logging
import re

from google.appengine.api import blobstore
from google.appengine.api.datastore_errors import BadValueError
from google.appengine.api.datastore_types import GeoPt
from google.appengine.ext import ndb
from google.appengine.ext.blobstore.blobstore import BlobInfo

from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.http import urlencode
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
import json

from pore.gallery.models import GalleryEntry, PhotoEntry
from pore.gallery.views import single


@require_POST
@never_cache
def get_upload_url(request):
    entry = {}
    for f in ('datestamp', 'location'):
        v = request.POST.get(f)
        if v:
            entry[f] = v

    notes = request.POST.get('notes')
    if notes:
        entry['public_note'] = notes

    if request.POST.get('gmap-location'):
        latlng = request.POST.get('latlng')
        if latlng:
            try:
                entry['latlng'] = GeoPt(latlng)
            except BadValueError, e:
                logging.warning(e, exc_info=1)

    msg = request.POST.get('message')
    if msg:
        msg = {
            'created': datetime.now().isoformat(),
            'message': msg,
        }
        email = request.POST.get('email')
        if email:
            msg['email'] = email
        entry['private_messages'] = [msg]

    entry = PhotoEntry(**entry)
    entry.put()
    logging.debug("Created %r" % entry.key)

    # authorize entry updating
    request.session['ups'] = request.session.get('ups', []) + [entry.key.id()]

    up_url = blobstore.create_upload_url(reverse(blobstore_callback, args=[entry.key.id()]))
    return http.HttpResponse(json.dumps({'url': up_url}), 'text/javascript')

@never_cache
def blobstore_callback(request, entry_id):
    info = None
    key_match = re.search(r"blob-key=([^;\r]+)[;\r]", request.body)
    if key_match:
        info = BlobInfo.get(key_match.group(1).strip('"'))
    if not info:
        return render(request, "upload.html", {'err': True})
    logging.info("Received file: %r" % ((info.filename, info.content_type, info.size, info.key()),))

    def tx(entry_id):
        entry = GalleryEntry.get_by_id(int(entry_id))
        if not entry:
            return render(request, "upload.html", {'err': True})
        if not entry.photos:
            entry.photos = [info.key()]
            # also publish the entry
            entry.tags = list(set(entry.tags + ['public']))
        else:
            entry.photos = entry.photos + [info.key()]
        entry.put()
        logging.debug("Updated %r" % entry.key)
        return http.HttpResponseRedirect("%s?%s" % (reverse(single, args=[entry.key.id()]),
                                                    urlencode({'ty': ''})))

    return ndb.transaction(lambda: tx(int(entry_id)))
