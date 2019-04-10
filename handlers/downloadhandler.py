from . import blobstore_handlers
from . import file_op


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        name = self.request.get('file_name')
        object = file_op.file_object(name)
        self.send_blob(object.blob)
