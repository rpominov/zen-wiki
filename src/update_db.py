from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from main import Page

class MainPage(webapp.RequestHandler):
	
	def get(self):
		for page in Page.all():
			page.private = not not page.private
			page.put()

application = webapp.WSGIApplication([('/_update_db', MainPage)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
