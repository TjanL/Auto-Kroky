import cherrypy, os

class HelloWorld(object):
	@cherrypy.expose
	def neki(self):
		return "Hello World!"


if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/html': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.abspath('./html')
		}
	}
	cherrypy.quickstart(HelloWorld(), '/', conf)