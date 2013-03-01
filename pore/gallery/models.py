from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class GalleryEntry(polymodel.PolyModel):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    tags = ndb.StringProperty(repeated=True)

    def is_public(self):
        return 'public' in self.tags

class PhotoEntry(GalleryEntry):
    photos = ndb.BlobKeyProperty(repeated=True)
    datestamp = ndb.StringProperty()
    public_note = ndb.TextProperty()
    location = ndb.StringProperty()
    latlng = ndb.GeoPtProperty()
    private_messages = ndb.JsonProperty()
