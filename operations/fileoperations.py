import logging
import directoryoperations as dirop
import useroperations as userop
from . import ndb
from . import File
from . import blobstore


def get_files_in_current_path():
    return dirop.get_current_directory_object().files


def file_object(file_name):
    user = userop.get_model_user()
    root_dir_object = dirop.get_current_directory_object()
    path = dirop.get_path(file_name,root_dir_object)
    id = user.key.id() + path
    key = ndb.Key(File,id)
    return key.get()

def  add(upload, filename):
    user = userop.get_model_user()
    current_dir = dirop.get_current_directory_object()
    id = user.key.id() + dirop.get_path(filename,current_dir)
    key = ndb.Key(File,id)
    if dirop.contains(key,current_dir.files):
        object = File(id=id)
        object.name = filename
        object.blob = upload.key()
        object.put()

        current_dir.files.append(key)
        current_dir.put()
    else:
        blobstore.delete(upload.key)
        logging.debug("A file with this name already exists in this directory!")

