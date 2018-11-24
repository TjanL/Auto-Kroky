import cherrypy
import glob
import os


class AutoKrokyServer(object):
	def __init__(self):
		# Preload html files
		self.html_files = {}
		for file in glob.glob("../html/*.html"):
			self.html_files[os.path.basename(file)] = open(file, encoding="utf8").read()

	def check_login(self):
		if not cherrypy.session.get("username"):
			raise cherrypy.HTTPRedirect("/login")

	@cherrypy.expose
	def index(self):
		self.check_login()
		return self.html_files["index.html"]

	@cherrypy.expose
	def profile(self):
		self.check_login()
		return self.html_files["profile.html"]

	@cherrypy.expose
	def preferences(self):
		self.check_login()
		return self.html_files["preferences.html"]

	@cherrypy.expose
	def login(self):
		cherrypy.session["username"] = "Tjan"
		return self.html_files["login.html"]

	@cherrypy.expose
	def logout(self):
		cherrypy.lib.sessions.expire()
		raise cherrypy.HTTPRedirect("/login")

	def error_page(status, message, traceback, version):
		return open(os.path.abspath("../html/404.html"), encoding="utf8").read()


if __name__ == '__main__':
	conf = {
	   '/': {
	       'tools.sessions.on': True,
	       'error_page.404': AutoKrokyServer.error_page
	    },
	    '/public': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('../public')
        }
	}

	cherrypy.quickstart(AutoKrokyServer(), '/', conf)