from . import ndb
from . import blobstore


class File(ndb.Model):
    # Name of the file as string
    # Data of the file
    name, blob, date = ndb.StringProperty(), ndb.BlobKeyProperty(), ndb.DateTimeProperty(auto_now_add=True)


def get_file_size(file_key):
    return blobstore.BlobInfo(file_key).size


def get_file_type(file_key):
    return blobstore.BlobInfo(file_key).content_type


def get_file_creation(file_key):
    return blobstore.BlobInfo(file_key).creation.strftime("%d %B %Y, %I:%M%p")


def get_file_name(file_key):
    return blobstore.BlobInfo(file_key).filename
