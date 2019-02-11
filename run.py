import os
import time
import cherrypy
import schedule
import threading

from lib import autokroky
from lib import server


class ScheduleThread(threading.Thread):
	def __init__(self):
		super(ScheduleThread, self).__init__()
		self.dirname = os.path.dirname(os.path.abspath(__file__))

	def order(self):
		obj = autokroky.Order(os.path.join(self.dirname, "database.db"))
		del obj

	def run(self):
		schedule.every().wednesday.at("12:00").do(self.order)

		while True:
			schedule.run_pending()
			time.sleep(60)


class WebServer(object):
	def __init__(self):
		self.dirname = os.path.dirname(os.path.abspath(__file__))
		self.root_conf = {
		   '/': {
				'tools.sessions.on': True,
				'error_page.default': server.Root.error_page
			},
			'/public': {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': os.path.join(self.dirname, 'public')
			}
		}

		self.api_conf = {
			'/': {
				'tools.sessions.on': True,
				'error_page.default': server.Api.error_page
				}
		}

	def run_server(self):
		cherrypy.tree.mount(server.Root(os.path.join(self.dirname, "html")), '/', self.root_conf)
		cherrypy.tree.mount(server.Api(os.path.join(self.dirname, "database.db")), '/api', self.api_conf)
		#cherrypy.server.socket_host = "192.168.1.11"
		cherrypy.server.socket_port = 80
		cherrypy.engine.start()


if __name__ == '__main__':
	ScheduleThread().start()
	WebServer().run_server()
