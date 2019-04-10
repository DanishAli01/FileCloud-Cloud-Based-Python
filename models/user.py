from . import ndb


class User(ndb.Model):
    # root directory key of user
    # current directory key of user
    root, c_dir = ndb.KeyProperty(), ndb.KeyProperty()

