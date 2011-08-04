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
        
class AddSubject(webapp.RequestHandler):
    def get (self):
        from google.appengine.ext import db
        subjects = db.GqlQuery("SELECT * FROM subjectdb ORDER BY subject ")
        depts = db.GqlQuery("SELECT * FROM departmentdb ORDER BY department")
        for dep in depts:
            dep.key = dep.key()
        
        template_values = {
            "subjects":subjects,
            "departments":depts,
        }
        path = os.path.join(os.path.split( 	os.path.dirname(__file__) ) [0] , 'html/add_subject.html' )
        self.response.out.write(template.render(path, template_values))
    def post (self):
        dept_key = self.request.get("Department")
        sub = self.request.get("NewSubject")
        python.models.subjectdb(
        department = python.models.departmentdb.get(dept_key),
        subject = sub,
        added_by = users.get_current_user()
        ).put()
        self.redirect("")
class AddQuestion(webapp.RequestHandler):
    def get_step1(self):
        template_values = {
                "departments":depts,
            }
    
    def get(self):
        if(self.request.get("DeptKey") == ""):
            depts = python.models.departmentdb.all()
            template_values = {
                "departments":depts,
            }
            path = os.path.join(os.path.split( 	os.path.dirname(__file__) ) [0] , 'html/add_question.html' )
            self.response.out.write(template.render(path, template_values))
            return
        else:
            from google.appengine.ext import db
            dept = self.request.get("DeptKey")
            #subjects = python.models.subjectdb.all().filter('department=', dept)
            template_values = {
                #"subjects":subjects,
            }
            path = os.path.join(os.path.split( 	os.path.dirname(__file__) ) [0] , 'html/add_question.html' )
            self.response.out.write(template.render(path, template_values))
            

def main():
    application = webapp.WSGIApplication([
											('/', IndexHandler),
											('/AddDepartment',AddDepartment),
                                            ('/AddSubject',AddSubject),
                                            ('/AddQuestion',AddQuestion),
										],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
