import datetime

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from operations import fileoperations as file_op


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    e = "e"
    def post(self):
        up = self.get_uploads()
        global e
        # upload all the files that came in the request
        for upload in up:
            # Get file name from the info of the file
            filename = blobstore.BlobInfo(upload.key()).filename
            e = file_op.add(upload, filename, datetime.datetime.now())

        self.redirect('/')

