from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from models.user import User
from models.dir import Folder
from models.file import File
import logging
import re