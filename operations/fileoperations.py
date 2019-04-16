import logging
from directoryoperations import get_path, contains, current_dir_obj
import useroperations as userop
from . import ndb
from models.file import File
from . import blobstore
from models.dir import Folder
import datetime
import models.file as m


def get_files_in_current_path():
    return current_dir_obj().files


def file_object(file_name):
    user = userop.get_model_user()
    root_dir_object = current_dir_obj()
    path = get_path(file_name, root_dir_object)
    id = user.key.id() + path
    return ndb.Key("File", id).get()
    # return key.get()


def add(upload, filename, datetime):
    user = userop.get_model_user()
    current_dir = current_dir_obj()
    id = user.key.id() + get_path(filename, current_dir)
    key = ndb.Key("File", id)

    if contains(key, current_dir.files):
        object = File(id=id)
        object.name = filename
        object.date = datetime
        object.blob = upload.key()
        object.put()
        current_dir.files.append(key)
        current_dir.put()
        return "file added!"
    else:
        blobstore.delete(upload.key())
        return "A file with this name already exists in this directory!"


def delete(name):
    user = userop.get_model_user()
    object = current_dir_obj()
    p = get_path(name, object)
    id = user.key.id() + p
    key = ndb.Key("File", id)
    blobobj = key.get().blob
    object.files.remove(key)
    blobstore.delete(blobobj)
    key.delete()
    object.put()


# def add_details(files):
#
#     for file in files:
#         key = file.key
#     return m.get_file_creation(key)
