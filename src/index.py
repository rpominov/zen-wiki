from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from main import Wiki

class MainPage(webapp.RequestHandler):
	
	def get(self):
		
		wiki = None
		user = users.get_current_user()
		if user:
			wiki = Wiki.getByUser(user)
		
		self.response.out.write(template.render('templates/index.html', {
			'user':       user,
			'logout_url': users.create_logout_url(self.request.path),
			'login_url':  users.create_login_url('/_onlogin'),
			'wiki':       wiki
		}))

application = webapp.WSGIApplication([('/', MainPage)])

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
