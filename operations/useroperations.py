import re

from . import users as ndbusers
from . import User as modeluser
from . import ndb
import directoryoperations as dirop
from . import Folder as modelfolder


# Get user from this page
def get_current_user():
    return ndbusers.get_current_user()


# Get user from model
def get_model_user():
    # Get current user
    user = get_current_user()
    if user:
        # retrive user from models using key
        user_key = ndb.Key(modeluser, user.user_id())
        return user_key.get()


# log in check
def is_user_logged_in():
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
    localuser = modeluser(id=user.userid())
    dirop.set_root_directory(user)
    localuser.current_dir = ndb.Key(modelfolder, localuser.key.id() + dirop.slash)
    localuser.put()


# extracts all the names from a list of directory/ file keys
def get_names_from_list(elements):
    names = list()

    for element in elements:
        names.append(element.get().name)

    return names


def prepare_directory_name(directory_name):
    return re.sub(r"[/;]", '', ' ', directory_name).lstrip()


def sort_list(list):
    return sorted(list, key=lambda item: item.get().name.lower())


def get_login_url(main_page):
    return ndbusers.create_login_url(main_page.request.uri)


def get_logout_url(main_page):
    return ndbusers.create_logout_url(main_page.request.uri)
