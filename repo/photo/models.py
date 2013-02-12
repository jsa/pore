from google.appengine.ext import ndb


class Photo(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    img_data = ndb.BlobKeyProperty(required=True)
