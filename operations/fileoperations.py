import logging
import directoryoperations as dirop
import useroperations as userop
from . import ndb
from . import File
from . import blobstore
from . import Folder
import datetime


def get_files_in_current_path():
    return dirop.current_dir_obj().files


def file_object(file_name):
    user = userop.get_model_user()
    root_dir_object = dirop.current_dir_obj()
    path = dirop.get_path(file_name, root_dir_object)
    id = user.key.id() + path
    key = ndb.Key(File, id)
    return key.get()


def add(upload, filename, datetime):
    user = userop.get_model_user()
    current_dir = dirop.current_dir_obj()
    id = user.key.id() + dirop.get_path(filename, current_dir)
    key = ndb.Key(File, id)
    if dirop.contains(key, current_dir.files):
        object = File(id=id)
        object.name = filename
        object.date = datetime
        object.blob = upload.key()
        object.put()

        current_dir.files.append(key)
        current_dir.put()
    else:
        blobstore.delete(upload.key)
        logging.debug("A file with this name already exists in this directory!")


def delete(name):
    user = userop.get_model_user()
    object = dirop.current_dir_obj()
    p = dirop.get_path(name, object)
    id = user.key.id() + p
    key = ndb.Key(File, id)
    blobobj = key.get().blob
    object.files.remove(key)
    blobstore.delete(blobobj)
    key.delete()
    object.put()


