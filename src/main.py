from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

import urllib

class Wiki(db.Model):
	user = db.UserProperty()
	url = db.StringProperty()
	
	@staticmethod
	def getByUser(user):
		wiki = Wiki.all().filter('user =', user).get()
		if not wiki:
			url = user.email().split('@')[0]
			while Wiki.getByUrl(url):
				url = '_' + url
			wiki = Wiki(url=url, user=user)
			wiki.put()
		return wiki
	
	@staticmethod
	def getByUrl(url):
		return Wiki.all().filter('url =', url).get()
	
	def getPage(self, url):
		return Page.all().ancestor(self).filter('url =', url).get()
	
	def canEdit(self):
		return self.user == users.get_current_user()
	
	def getUrl(self):
		return '/' + urllib.quote(self.url.encode('utf-8'))
	
	def allPages(self):
		return  Page.all().ancestor(self).fetch(1000)
		
	
class Page(db.Model):
	url = db.StringProperty()
	content = db.TextProperty()
	
	def title(self):
		return self.url.split('/')[-1] or 'root'
	
	def getUrl(self):
		return '/' + urllib.quote(self.url.encode('utf-8'))

class MainPage(webapp.RequestHandler):
	
	def get(self):
		path = urllib.unquote(self.request.path)
		wikiurl = path.split('/')[1]
		pageurl = '/'.join(filter(lambda x: not not x, path.split('/')[2:]))
		
		wiki = Wiki.getByUrl(wikiurl)
		
		if not wiki:
			self.e404()
			return
		
		page = wiki.getPage(pageurl)
		
		if not page:
			if wiki.canEdit():
				page = Page(url=pageurl, content='', parent=wiki)
			else:
				self.e404()
				return
			
		urls = []
		for p in wiki.allPages():
			urls.append(p.url)
			
		menu = {}
		for url in urls:
			_path = url.split('/')
			cur = menu
			cur_path = ''
			for step in _path:
				if cur_path:
					cur_path += '/' + step
				else:
					cur_path += step
				if not step in cur.keys():
					cur[step] = {'is_page': cur_path in urls, 'children': {} }
				cur = cur[step]['children']
			
		self.response.out.write(template.render('templates/main.html', {
			'user':       users.get_current_user(),
			'logout_url': users.create_logout_url(self.request.path),
			'login_url':  users.create_login_url(self.request.path),
			'wiki':       wiki,
			'pages':      wiki.allPages(),
			'page':       page,
			'path':       filter(lambda x: not not x, path.split('/')[1:-1])
		}))
		
	def post(self):
		path = urllib.unquote(self.request.path)
		wikiurl = path.split('/')[1]
		pageurl = '/'.join(filter(lambda x: not not x, path.split('/')[2:]))
		
		wiki = Wiki.getByUrl(wikiurl)
		
		if not wiki:
			self.e404()
			return
		
		if wiki.canEdit():
			
			page = wiki.getPage(pageurl)
			if not page:
				page = Page(url=pageurl, content='', parent=wiki)
			
			move = self.request.get('move', default_value='')
			delete = self.request.get('delete', default_value=0)
			
			if delete:
				if page.is_saved():
					page.delete()
				self.redirect(wiki.getUrl())
			elif move:
				page.url = move
				page.put()
				self.redirect(wiki.getUrl() + page.getUrl())
			else:
				page.content = self.request.get('content', default_value='')
				page.put()
				self.redirect(self.request.path)
		else:
			self.e403()
			return
			
	def e404(self):
		self.error(404)
		self.response.out.write(template.render('templates/error.html', {'error': '404 not found ;('}))
		
	def e403(self):
		self.error(404)
		self.response.out.write(template.render('templates/error.html', {'error': '403 forbidden ;('}))


application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)


def main():
	run_wsgi_app(application)


if __name__ == "__main__":
	main()
