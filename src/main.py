from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from django.utils.text import capfirst
from django.utils.html import escape

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
		result = Page.all().ancestor(self).filter('url =', url)
		if not self.canEdit():
			result.filter('private =', False)
		return result.get()

	def canEdit(self):
		return self.user == users.get_current_user()

	def getUrl(self):
		return '/' + urllib.quote(self.url.encode('utf-8'))

	def allPages(self):
		result = Page.all().ancestor(self)
		if not self.canEdit():
			result.filter('private =', False)
		return result.fetch(1000)

class Page(db.Model):
	url = db.StringProperty()
	content = db.TextProperty()
	private = db.BooleanProperty()

	def title(self):
		return self.url.split('/')[-1] or 'root'

	def getUrl(self):
		return '/' + urllib.quote(self.url.encode('utf-8'))

class MainPage(webapp.RequestHandler):

	def get(self):
		path = filter(lambda x: not not x, urllib.unquote(self.request.path).decode('utf8').split('/'))
		wikiurl = path[0]
		pageurl = '/'.join(path[1:])

		wiki = Wiki.getByUrl(wikiurl)

		if not wiki:
			self.e404()
			return

		page = wiki.getPage(pageurl)

		if not page:
			page = Page(url=pageurl, content='', parent=wiki, private=False)

		# ---------- menu building
		pages = {}
		for p in wiki.allPages():
			pages[p.url] = p
		urls = pages.keys()

		menu = {}
		for url in urls:
			if not url: continue # drop 'Root'
			_path = url.split('/')
			cur = menu
			cur_path = ''
			for step in _path:
				cur_path += ('/' if cur_path else '') + step
				if not step in cur.keys():
					cur[step] = {
						'is_page': cur_path in urls,
						'private': cur_path in urls and pages[cur_path].private,
						'current': (wiki.getUrl() + '/' + cur_path) == ('/' + '/'.join(path)),
						'children': {}
					}
				cur = cur[step]['children']

		cur_path = ''
		menu = {u'': {
			'is_page': cur_path in urls,
			'private': cur_path in urls and pages[cur_path].private,
			'current': (wiki.getUrl() + cur_path) == ('/' + '/'.join(path)),
			'children': menu
		}}

		def draw(root, url_prefix):
			result = ''
			for url_part in sorted(root.keys()):

				item = root[url_part]

				name = url_part or 'root'
				name = capfirst(name)
				name = escape(name)

				url = url_prefix + url_part

				class_name = ''
				if not item['is_page']: class_name += ' new'
				if     item['current']: class_name += ' current'
				if     item['private']: class_name += ' private'

				children = ''
				if item['children']:
					children = '<ul>%s</ul>' % draw(item['children'], url_prefix + url_part + '/')

				result += '<li><span class="name %s"><a href="%s">%s</a></span>%s</li>' % (class_name, url, name, children)

			return result

		menu_html = draw(menu, wiki.getUrl())
		# ----------

		breadcrumbs = path[:-1]
		if len(breadcrumbs):
			breadcrumbs[0] = 'root'

		self.response.out.write(template.render('templates/main.html', {
			'user':       users.get_current_user(),
			'logout_url': users.create_logout_url(self.request.path),
			'login_url':  users.create_login_url(self.request.path),
			'wiki':       wiki,
			'page':       page,
			'path':       breadcrumbs,
			'menu_html':  menu_html
		}))

	def post(self):
		path = filter(lambda x: not not x, urllib.unquote(self.request.path).decode('utf8').split('/'))
		wikiurl = path[0]
		pageurl = '/'.join(path[1:])

		wiki = Wiki.getByUrl(wikiurl)

		if not wiki:
			self.e404()
			return

		if wiki.canEdit():

			page = wiki.getPage(pageurl)
			if not page:
				page = Page(url=pageurl, content='', parent=wiki, private=False)

			move = self.request.get('move', default_value='')
			delete = self.request.get('delete', default_value=0)
			private = self.request.get('private', default_value=None)

			if private:
				page.private = (private == '1')
				page.put()
				self.redirect(self.request.path)
			elif delete:
				if page.is_saved():
					page.delete()
				self.redirect(wiki.getUrl())
			elif move:
				page.url = '/'.join(filter(lambda x: not not x, move.split('/')))
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


application = webapp.WSGIApplication([('/.*', MainPage)])


def main():
	run_wsgi_app(application)


if __name__ == "__main__":
	main()

