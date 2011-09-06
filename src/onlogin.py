from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from main import Wiki

class MainPage(webapp.RequestHandler):
	
	def get(self):
		user = users.get_current_user()
		
		if user:
			wiki = Wiki.getByUser(user)
			self.redirect(wiki.getUrl())
		else:
			self.redirect('/')

application = webapp.WSGIApplication([('/_onlogin', MainPage)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
