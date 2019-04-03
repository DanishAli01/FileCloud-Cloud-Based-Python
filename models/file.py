from google.appengine.ext import ndb


class File(ndb.Model):
    # Name of the file as string
    # Data of the file
    name, blob = ndb.StringProperty(), ndb.BlobKeyProperty()
