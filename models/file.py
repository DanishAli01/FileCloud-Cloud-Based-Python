from . import ndb


class File(ndb.Model):
    # Name of the file as string
    # Data of the file
    name, blob, date = ndb.StringProperty(), ndb.BlobKeyProperty(), ndb.DateTimeProperty(auto_now_add=True)

