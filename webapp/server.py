import cherrypy

class AutoKroky(object):

	@cherrypy.expose
	def index(self):
		if not cherrypy.session.get("username"):
			raise cherrypy.HTTPRedirect("/profile")
		return open("index.html", encoding="utf8")

	@cherrypy.expose
	def profile(self):
		cherrypy.session['username'] = "dasd"
		return open("profile.html", encoding="utf8")

	@cherrypy.expose
	def preferences(self):
		return open("preferences.html")

	@cherrypy.expose
	def logout(self):
		cherrypy.lib.sessions.expire()


if __name__ == '__main__':
	conf = {
	   '/': {
	       'tools.sessions.on': True
	    }
	}

	cherrypy.quickstart(AutoKroky(), '/', conf)