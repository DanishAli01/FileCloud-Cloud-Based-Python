from . import blobstore_handlers
from . import file_op
from . import blobstore

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        up = self.get_uploads()

        # upload all the files that came in the request
        for upload in up:
            # Get file name from the info of the file
            filename = blobstore.BlobInfo(upload.key()).filename

            file_op.add(upload, filename)

        self.redirect('/')