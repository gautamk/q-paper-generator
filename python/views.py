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
        #Get Department
        depts = python.models.departmentdb.all()
        for dep in depts:
            dep.key = dep.key()
        template_values = {
                "departments":depts,
            }
        path = os.path.join(os.path.split(     os.path.dirname(__file__) ) [0] , 'html/add_question.html' )
        self.response.out.write(template.render(path, template_values))
        
    def get_step2(self):
        #Get Subject
        from google.appengine.ext import db
        dept = self.request.get("DeptKey")
        subjects = python.models.subjectdb.all().filter('department = ', db.Key(dept))
        template_values = {
            "subjects":subjects,
        }
        path = os.path.join(os.path.split(     os.path.dirname(__file__) ) [0] , 'html/add_question.html' )
        self.response.out.write(template.render(path, template_values))
    
    def get(self):
        if(self.request.get("DeptKey") == ""):
            self.get_step1()
        else:
            self.get_step2()
            
class QuestionForm(webapp.RequestHandler):
    def post (self):
        import re
        sub_key = self.request.get("SubKey")
        q_type = self.request.get("QuestionType")
        questions_added_counter = 0
        args=self.request.arguments() # get the names of the arguments
        
        for i in range(args.__len__()): # Loop Through each Argument name 
            if(args[i].count("question")): # check if the argument is a question
                #Add the question to the database.
                if(self.request.get(args[i]) != ""):
                    python.models.questiondb( subject = python.models.subjectdb.get(sub_key) ,
                                              question_type = q_type,
                                              question =self.request.get(args[i]) ,
                                              added_by = users.get_current_user()
                                              ).put()
                    questions_added_counter += 1
        self.response.out.write(str(questions_added_counter)+" Questions Added")
                                          
        
        
    def get(self):
        from google.appengine.ext import db
        SubKey = self.request.get("SubKey")
        
        try:
            NumberOfQuestions = int(self.request.get("NumberOfQuestions"))
        except ValueError:
            #if a non numeric or empty value is given
            NumberOfQuestions = 1
            
        QuestionType = self.request.get("QuestionType")
        
        if( (SubKey=="")  or (QuestionType == "") ):
            self.response.out.write("Required parameters missing")
        else:
            template_values = {
            "sub_key":SubKey,
            "question_type":QuestionType,
            "count":range(NumberOfQuestions),
            "number_of_questions":NumberOfQuestions,
            }
            path = os.path.join(os.path.split(     os.path.dirname(__file__) ) [0] , 'html/question_form.html' )
            self.response.out.write(template.render(path, template_values))
        

def main():
    application = webapp.WSGIApplication([
											('/', IndexHandler),
											('/AddDepartment',AddDepartment),
                                            ('/AddSubject',AddSubject),
                                            ('/AddQuestion',AddQuestion),
                                            ('/QuestionForm',QuestionForm),
										],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
