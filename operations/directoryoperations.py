from . import users as ndbusers
from . import User as modeluser
from . import  Folder as modelfolder
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

