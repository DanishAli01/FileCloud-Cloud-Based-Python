from operations import useroperations
from models.dir import Folder as modelfolder
from . import ndb

slash = "/"
rootname = "root"


# returns key of current directory
def current_dir_obj():
    return get_current_directory_key().get()


# returns key of current directory
def get_current_directory_key():
    user = useroperations.get_model_user()
    return user.c_dir


# returns key of root directory
def get_parent_directory_key():
    return get_current_directory_key().get().root_dir


def set_root_directory(my_user):
    directory_id = my_user.key.id() + slash
    directory = modelfolder(id=directory_id)

    directory.parent_directory = None
    directory.name = rootname
    directory.path = slash
    directory.put()

    my_user.root_directory = directory.key
    my_user.put()


def get_directories_in_current_path():
    return current_dir_obj().drs


# returns true if current directory is root directory
def is_in_root_directory():
    current_directory = current_dir_obj()
    return True if current_directory.root_dir is None else False


def get_path(n, parent_dir_object):
    if is_in_root_directory():
        return parent_dir_object.path + n
    else:
        return parent_dir_object.path + slash + n


def dir_is_empty_check(dir):
    return not dir.files and not dir.drs


# checks if a key is in a list of keys, if so returns true
def contains(key, list):
    return key not in list


def add_dir(name, parent):
    user = useroperations.get_model_user()
    parent_object = parent.get()
    p = get_path(name, parent_object)
    id = user.key.id() + p
    dir = modelfolder(id=id)
    dir_key = dir.key

    if contains(dir_key, parent_object.drs):
        parent_object.drs.append(dir_key)
        parent_object.put()
        # Set all attributes of the directory and save it to datastore
        dir.root_dir = parent
        dir.name = name
        dir.path = p
        dir.put()


def delete_dir(name):
    my_user = useroperations.get_model_user()

    # current directory is the parent directory of the one that will be deleted
    parent_directory_object = current_dir_obj()

    directory_id = my_user.key.id() + get_path(name, parent_directory_object)
    directory_key = ndb.Key(modelfolder, directory_id)
    directory_object = directory_key.get()

    if dir_is_empty_check(directory_object):
        # Delete reference to this object from parent_directory
        parent_directory_object.drs.remove(directory_key)
        parent_directory_object.put()

        # Delete directory object from datastore
        directory_key.delete()


def home():
    user = useroperations.get_model_user()
    user.c_dir = ndb.Key(modelfolder, user.key.id() + slash)
    user.put()


def nav_dir(name):
    user = useroperations.get_model_user()
    path = user.key.id() + get_path(name, current_dir_obj())
    key = ndb.Key(modelfolder, path)
    user.c_dir = key
    user.put()
