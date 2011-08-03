import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import users
import python.models
class IndexHandler(webapp.RequestHandler):
    def get(self):
        template_values = {
            "logout_url":users.create_logout_url('/'),
            "username":users.get_current_user(),
            
            }
        path = os.path.join(os.path.split( 	os.path.dirname(__file__) ) [0] , 'html/index.html' )
        self.response.out.write(template.render(path, template_values))
class AddDepartment(webapp.RequestHandler):
    def get (self):
        depts = python.models.departmentdb.all()
        template_values = {
            "departments":depts,
        }
        path = os.path.join(os.path.split( 	os.path.dirname(__file__) ) [0] , 'html/add_department.html' )
        self.response.out.write(template.render(path, template_values))
    def post(self):
        python.models.departmentdb(
            department = self.request.get("NewDepartment") ,
            added_by = users.get_current_user(),
            ).put()
        self.redirect("")

def main():
    application = webapp.WSGIApplication([
											('/', IndexHandler),
											('/AddDepartment',AddDepartment),
										],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
