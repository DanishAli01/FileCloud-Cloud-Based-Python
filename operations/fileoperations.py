import useroperations as userop
from directoryoperations import get_path, contains, current_dir_obj, add_dir
from models.file import File
from . import blobstore
from . import ndb


def get_files_in_current_path():
    return current_dir_obj().files


def get_files_number_in_current_path():
    return len(current_dir_obj().files)


def file_object(file_name):
    user = userop.get_model_user()
    root_dir_object = current_dir_obj()
    path = get_path(file_name, root_dir_object)
    id = user.key.id() + path
    return ndb.Key("File", id).get()


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


#
# def share(upload, filename, key, datetime):
#     model_user_from_key = ndb.Key("User", key).get()
#     add_dir("Shared", model_user_from_key.root)
#     current_dir_obj_from_shared = model_user_from_key..get()
#     id = model_user_from_key.key.id() + get_path(filename,current_dir_obj_from_shared)
#     fkey = ndb.Key("File",id)


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
