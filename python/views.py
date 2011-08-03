import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import users


class IndexHandler(webapp.RequestHandler):
    def get(self):
        template_values = {
            "LogoutUrl":users.create_logout_url('/'),
            }
        path = os.path.join(os.path.split( 	os.path.dirname(__file__) ) [0] , 'html/index.html' )
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([
											('/', IndexHandler),
											#('/AddQuestion',AddQuestion),
										],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
