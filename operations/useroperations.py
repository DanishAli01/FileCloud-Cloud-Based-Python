import re

from . import users as ndbusers
from models.user import User
from . import ndb
import directoryoperations as fromdirectoryoperations
from models.dir import Folder as modelfolder
import models.file


# Get user from this page
def get_current_user():
    return ndbusers.get_current_user()


# Get user from model
def get_model_user():
    # Get current user
    user = get_current_user()
    if user:
        # retrive user from models using key
        user_key = ndb.Key("User", user.user_id())
        return user_key.get()


# log in check
def login_check():
    if get_current_user():
        return True
    else:
        return False


# returns true if for this user
# a myuser object already exists in the datastore
def user_present_in_model():
    if get_model_user():
        return True
    else:
        return False


def add_user(user):
    my_user = User(id=user.user_id())
    fromdirectoryoperations.set_root_directory(my_user)

    # set current path on first login to root directory
    my_user.c_dir = ndb.Key("Folder", my_user.key.id() + fromdirectoryoperations.slash)
    my_user.put()


# extracts all the names from a list of directory/ file keys
def get_names_from_list(elements):
    names = list()

    for element in elements:
        names.append(element.get().name)
    return names


def get_file_size(files):
    size = list()
    for e in files:
        size.append(models.file.get_file_size(e.get().blob))
    return size


def get_total_totalsize(files):
    totalsize = 0;
    for e in files:
        totalsize += models.file.get_file_size(e.get().blob)
    return totalsize;


def get_file_creation(files):
    size = list()
    for e in files:
        size.append(models.file.get_file_creation(e.get().blob))
    return size


def get_file_kind(files):
    size = list()
    for e in files:
        size.append(models.file.get_file_type(e.get().blob))
    return size


def sort_list(list):
    return sorted(list, key=lambda item: item.get().name.lower())


def get_login_url(main_page):
    return ndbusers.create_login_url(main_page.request.uri)


def get_logout_url(main_page):
    return ndbusers.create_logout_url(main_page.request.uri)
