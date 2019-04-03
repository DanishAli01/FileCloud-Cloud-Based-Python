from google.appengine.ext import ndb


class User(ndb.Model):
    # root directory key of user
    # current directory key of user
    root_dir, current_dir = ndb.KeyProperty(), ndb.KeyProperty()

