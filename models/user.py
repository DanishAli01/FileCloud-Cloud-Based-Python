from . import ndb


class User(ndb.Model):
    # root directory key of user
    # current directory key of user
    root, current_dir = ndb.KeyProperty(), ndb.KeyProperty()

