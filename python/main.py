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
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.ext.webapp import template
from google.appengine.api import users

 	
class Dept(polymodel.PolyModel):
	dept_name = db.StringProperty(required = True)

class Subject (Dept):
	subject_name = db.StringProperty(required = True)

class Question(Subject):
	question = db.TextProperty(required = True)
	answer = db.TextProperty(required = True)
	author = db.UserProperty()
	date = db.DateTimeProperty(auto_now = True)
	question_type=db.StringProperty(required = True)

	
	


class MainHandler(webapp.RequestHandler):
    def get(self):
		user = users.get_current_user()
		result=Dept.all()
		#result.order('-date')
		
		template_values = {
		"LogoutUrl":users.create_logout_url('/'),
		"QList" : result,	
		"QListLength" : result.count(),	
		}
		path = os.path.join(os.path.split( 	os.path.dirname(__file__) ) [0] , 'html/main.html' )
		self.response.out.write(template.render(path, template_values))

class AddQuestion(webapp.RequestHandler):
	def post(self):
		try:
			dept_name=self.request.get('dept_name')
			subject_name = self.request.get('subject_name')
			question_type = self.request.get('question_type')
			question = self.request.get('question')
			answer = self.request.get('answer')
			Question(
					dept_name=dept_name,
					subject_name=subject_name,
					question_type = question_type,
					question = question,
					answer = answer , 
					author = users.get_current_user(),
					).put()
			self.redirect("/")	
		except db.BadValueError:
			self.response.out.write( "There were some Missing Values in your Question , Please press the back button and correct it . and try again")

def main():
    application = webapp.WSGIApplication([
											('/', MainHandler),
											('/AddQuestion',AddQuestion),
										],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
