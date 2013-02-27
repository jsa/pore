import re

from google.appengine.api import images
from google.appengine.api.blobstore.blobstore import BLOB_KEY_HEADER
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from google.appengine.ext.ndb.blobstore import BlobInfo

from django import http
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from repo.util import render_to

from .models import GalleryEntry, PhotoEntry


def _apply_img_params(img, params):
    m = re.match('^-(\d+)$', params)
    if m:
        img.resize(int(m.group(1)))

@require_GET
@cache_control(public=True, max_age=4 * 7 * 24 * 60 * 60)
def photo(request, entry_id, photo_n, params):
    entry = ndb.Key(PhotoEntry, int(entry_id)).get()
    if not entry or 'hidden' in entry.tags:
        raise http.Http404, "Entry %r not found" % (entry_id,)

    blob_key = entry.photos[int(photo_n)]
    blob_info = BlobInfo.get(blob_key)

    if not params:
        rs = http.HttpResponse('', blob_info.content_type)
        rs[BLOB_KEY_HEADER] = blob_key
        return rs

    img = images.Image(blob_key=blob_key)
    if params:
        _apply_img_params(img, params)
    img.im_feeling_lucky()
    img_data = img.execute_transforms(output_encoding=images.JPEG)

    return http.HttpResponse(img_data, blob_info.content_type)

@require_GET
@render_to("gallery.html")
def browse(request):
    context = {}
    # man, this paging is hard...
    fwd, prev = request.GET.get('next'), request.GET.get('prev')
    qry = GalleryEntry.query(GalleryEntry.tags == 'public')
    if fwd:
        page, next_cursor, more = qry.order(-GalleryEntry.created) \
                                     .fetch_page(20, start_cursor=Cursor(urlsafe=fwd))
        context.update({
            'batch': page,
            'paging': {
                'prev': fwd,
                'next': next_cursor.urlsafe(),
                'is_first': False,
                'is_last': not more,
            },
        })

    elif prev:
        page, next_cursor, less = qry.order(GalleryEntry.created) \
                                     .fetch_page(20, start_cursor=Cursor(urlsafe=prev).reversed())
        context.update({
            'batch': page[::-1],
            # normalize the cursor direction
            'paging': {
                'prev': next_cursor.reversed().urlsafe(),
                'next': prev,
                'is_first': not less,
                'is_last': False,
            },
        })

    else:
        page, next_cursor, more = qry.order(-GalleryEntry.created) \
                                     .fetch_page(20)
        paging = {'is_first': True}
        if more:
            paging.update({
                'next': next_cursor.urlsafe(),
                'is_last': False,
            })
        else:
            paging['is_last'] = True
        context.update({
            'batch': page,
            'paging': paging,
        })

    return context

@require_GET
@render_to("photo.html")
def single(request, entry_id):
    entry = ndb.Key(GalleryEntry, int(entry_id)).get()
    if not entry:
        raise http.Http404, "Entry %r not found" % (entry_id,)
    ctx = {}
    ref = request.META.get('HTTP_REFERER')
    if ref:
        ctx['back'] = ref
    if 'ty' in request.GET:
        ctx['thankyou'] = True
    if entry.key.id() in request.session.get('ups', []):
        ctx['admin'] = True
    return ctx
