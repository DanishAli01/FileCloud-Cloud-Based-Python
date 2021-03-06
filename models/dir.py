from . import ndb



class Folder(ndb.Model):
    # name & path
    name, path = ndb.StringProperty(), ndb.StringProperty()

    # The key of the directory to navigate and interact with root
    # all sub directories of given directory
    # keys of all the files in given directory
    root_dir, directs, files = ndb.KeyProperty(), ndb.KeyProperty(repeated=True), ndb.KeyProperty(repeated=True)

    # def delete_directs_name(self, name):
    #     self.directs.remove(name)
