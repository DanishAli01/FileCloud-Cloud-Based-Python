import jinja2
import os
import operations.useroperations

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render_login(self, url):
    template = JINJA_ENVIRONMENT.get_template('/template/login.html')
    self.response.write(template.render({'url': url}))


def render_error(self, url,error):
    template = JINJA_ENVIRONMENT.get_template('/template/error.html')
    self.response.write(template.render({'url': url,'error': error}))


def render_main(self, url, dirs, files,size,create,kind,length,totalsize,totalfiles,totaldirs,current_path, is_in_root, upload_url):
    template = JINJA_ENVIRONMENT.get_template('/template/main.html')
    self.response.write(template.render({'url': url,
                                         'user': operations.useroperations.get_current_user(),
                                         'directories': dirs,
                                         'files': files,
                                         'size' : size,
                                         'create': create,
                                         'kind' : kind,
                                         'len': length,
                                         'totalSize':totalsize,
                                         'totalFiles': totalfiles,
                                         'totalDirs': totaldirs,
                                         'current_path': current_path,
                                         'is_not_in_root': not is_in_root,
                                         'upload_url': upload_url}))
