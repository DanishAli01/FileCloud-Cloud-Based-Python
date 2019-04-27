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
import re
import webapp2
import display
from handlers import blobstore
from handlers import downloadhandler, uploadhandler
from models.dir import Folder
from operations import fileoperations, useroperations, directoryoperations
from operations import ndb


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        if useroperations.login_check():
            if not useroperations.user_present_in_model():
                useroperations.add_user(useroperations.get_current_user())
            if self.request.get('directory_name') != '':
                directoryoperations.nav_dir(self.request.get('directory_name'))
                self.redirect('/')

            dir_names = useroperations.get_names(directoryoperations.get_directories_in_current_path())
            file_names = useroperations.get_names(fileoperations.get_files_in_current_obj())
            file_size = useroperations.get_file_size(fileoperations.get_files_in_current_obj())
            file_create = useroperations.get_file_creation(fileoperations.get_files_in_current_obj())
            file_kind = useroperations.get_file_kind(fileoperations.get_files_in_current_obj())
            total_size = useroperations.get_total_totalsize(fileoperations.get_files_in_current_obj())
            total_files = fileoperations.get_files_number_in_current_path()
            total_dirs = directoryoperations.get_total_directories_in_current_path()
            length = len(file_names)


            display.render_main(self,
                                useroperations.get_logout_url(self),
                                dir_names,
                                file_names,
                                file_size,
                                file_create,
                                file_kind,
                                length,
                                total_size,
                                total_files,
                                total_dirs,
                                directoryoperations.current_dir_obj().path,
                                directoryoperations.is_in_root_directory(),
                                blobstore.create_upload_url('/upload'))

        else:
            display.render_login(self, useroperations.get_login_url(self))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        button_value = self.request.get('button')

        if button_value == 'Add':
            absolute_name = re.sub(r"[/;]", '', self.request.get('value')).lstrip()
            if not (absolute_name is None or absolute_name == ''):
                directoryoperations.add_dir(absolute_name, directoryoperations.get_current_directory_key())
            self.redirect('/')

        elif button_value == 'Delete':
            name, kind = self.request.get('name'), self.request.get('kind')
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
