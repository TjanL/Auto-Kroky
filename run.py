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
		autokroky.Order.run(os.path.join(self.dirname, "database.db"))

	def run(self):
		schedule.every().tuesday.at("12:00").do(self.order)

		while True:
			schedule.run_pending()
			time.sleep(60)


class WebServer(object):
	def __init__(self):
		self.dirname = os.path.dirname(os.path.abspath(__file__))

		self.root = server.Root(os.path.join(self.dirname, "html"))
		self.api = server.Api(os.path.join(self.dirname, "database.db"))

		self.root_conf = {
		   '/': {
				'tools.sessions.on': True,
				'error_page.default': self.root.error_page
			},
			'/public': {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': os.path.join(self.dirname, 'public')
			}
		}

		self.api_conf = {
			'/': {
				'tools.sessions.on': True,
				'error_page.default': self.api.error_page
				}
		}

	def run_server(self):
		cherrypy.tree.mount(self.root, '/', self.root_conf)
		cherrypy.tree.mount(self.api, '/api', self.api_conf)
		cherrypy.server.socket_port = 80
		cherrypy.engine.start()


if __name__ == '__main__':
	ScheduleThread().start()
	WebServer().run_server()
