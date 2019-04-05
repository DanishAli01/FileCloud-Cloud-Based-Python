from . import users as ndbusers
from . import User as modeluser
from . import Folder as modelfolder
from . import ndb
import useroperations as userop


slash = "/"
rootname = "root"


# returns key of current directory
def get_current_directory_object():
    return get_current_directory_key().get()


# returns key of current directory
def get_current_directory_key():
    user = userop.get_model_user()
    return user.current_dir


def set_root_directory(user):
    new_dir_id = user.key.id() + slash
    dir = modelfolder(id=new_dir_id)
    dir.root_dir = None
    dir.name = rootname
    dir.path = slash
    dir.put()
    user.root_dir
    user.put()


def get_dirs_in_current_path():
    return get_current_directory_object().drs


# returns true if current directory is root directory
def is_in_root_directory():
    current_directory = get_current_directory_object()
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

def add_dir(name,parent):
    user = userop.get_model_user()
    parent_object = parent.get()
    p = get_path(name,parent_object)
    id = user.get.key.id() + p
    dir = modelfolder(id=id)
    dir_key = dir.key

    if contains(dir_key,parent_object.drs):
        parent_object.drs.append(dir_key)
        parent_object.put()

        # Set all attributes of the directory and save it to datastore
        dir.root_dir = parent
        dir.name = name
        dir.path = p
        dir.put()

