#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import datetime

import webapp2
import re
from handlers import downloadhandler,uploadhandler
from operations import fileoperations, useroperations, directoryoperations
from handlers import blobstore
from operations import ndb
from models.dir import Folder
from  models.file import File
import Display



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        if useroperations.login_check():
            if not useroperations.user_present_in_model():
                useroperations.add_user(useroperations.get_current_user())
            if self.request.get('directory_name') != '':
                directoryoperations.nav_dir(self.request.get('directory_name'))

            sort_dir = useroperations.sort_list(directoryoperations.get_directories_in_current_path())
            sort_files = useroperations.sort_list(fileoperations.get_files_in_current_path())
            sort_dir_names = useroperations.get_names_from_list(sort_dir)
            sort_file_names = useroperations.get_names_from_list(sort_files)
            sort_file_size = useroperations.get_file_size(sort_files)
            sort_file_create = useroperations.get_file_creation(sort_files)
            sort_file_kind = useroperations.get_file_kind(sort_files)
            length = len(sort_file_names)


            Display.render_main(self,
                                useroperations.get_logout_url(self),
                                sort_dir_names,
                                sort_file_names,
                                sort_file_size,
                                sort_file_create,
                                sort_file_kind,
                                length,
                                directoryoperations.current_dir_obj().path,
                                directoryoperations.is_in_root_directory(),
                                blobstore.create_upload_url('/upload'))

        else:
            Display.render_login(self, useroperations.get_login_url(self))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        button_value = self.request.get('button')

        if button_value == 'Add':
            absolute_name = re.sub(r"[/;]", '',self.request.get('value')).lstrip()
            if not (absolute_name is None or absolute_name == ''):
                directoryoperations.add_dir(absolute_name,directoryoperations.get_current_directory_key())
            self.redirect('/')

        elif button_value == 'Delete':
            name,kind = self.request.get('name'),self.request.get('kind')
            if kind == 'file':
                fileoperations.delete(name)
            elif kind == 'directory':
                directoryoperations.delete_dir(name)
            self.redirect('/')

        elif button_value == 'Up':
            user = useroperations.get_model_user()
            if not directoryoperations.is_in_root_directory():
                user.c_dir = directoryoperations.get_parent_directory_key()
                user.put()
            self.redirect('/')

        elif button_value == 'Home':
            user = useroperations.get_model_user()
            user.c_dir = ndb.Key(Folder, user.key.id() + directoryoperations.slash)
            user.put()
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', uploadhandler.UploadHandler),
    ('/download', downloadhandler.DownloadHandler)
], debug=True)
