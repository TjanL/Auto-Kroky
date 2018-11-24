import cherrypy
import glob
import os
import MySQLdb
from passlib.hash import pbkdf2_sha256
import kroky_lib2


class WebServer(object):
	def __init__(self, root_dir):
		self.root_dir = root_dir

		# Preload html files
		self.html_files = {}
		for file in glob.glob("../html/*.html"):
			self.html_files[os.path.basename(file)] = open(file, encoding="utf8").read()

	@cherrypy.tools.register("before_handler")
	def require_auth():
		if not cherrypy.session.get("username"):
			raise cherrypy.HTTPRedirect("/login")

	@cherrypy.expose
	@cherrypy.tools.require_auth()
	def index(self):
		return self.html_files["index.html"]

	@cherrypy.expose
	@cherrypy.tools.require_auth()
	def profile(self):
		return self.html_files["profile.html"]

	@cherrypy.expose
	@cherrypy.tools.require_auth()
	def preferences(self):
		return self.html_files["preferences.html"]

	@cherrypy.expose
	def login(self):
		return self.html_files["login.html"]

	@cherrypy.expose
	def logout(self):
		cherrypy.lib.sessions.expire()
		raise cherrypy.HTTPRedirect("/login")

	def error_page(status, message, traceback, version):
		return open(os.path.abspath("../html/404.html"), encoding="utf8").read()


class Api(object):
	def __init__(self, db_user, db_password, database, db_ip="localhost"):
		self._db = MySQLdb.connect(db_ip, db_user, db_password, database, charset='utf8')
		self._cursor = db.cursor()

	def error_page(status, message, traceback, version):
		return status

	@cherrypy.tools.register("before_handler")
	def require_auth(self):
		if not cherrypy.session.get("id"):
			return {"error": "Not logged in!"}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["GET"])
	def login(self, username, password):
		if username and password:
			stmt = "SELECT username, password, id FROM users WHERE username = %s"
			self._cursor.execute(stmt, [username])
			user, hash_pass, user_id = cursor.fetchone()

			if pbkdf2_sha256.verify(password, hash_pass):
				cherrypy.session["username"] = username
				cherrypy.session["id"] = user_id
				raise cherrypy.HTTPRedirect("/")

		return {"error": "Username or password incorrect!"}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["GET"])
	def register(self, username, password, c_password, k_username, k_password):
		if username:
			stmt = "SELECT id FROM users WHERE username = %s"
			self._cursor.execute(stmt, [username])
			if self._cursor.fetchone():
				return {"error": "Username already taken!"}

		elif password:
			if len(password) < 6:
				return {"error": "Password must have atleast 6 characters"}
			elif c_password != password:
				return {"error": "Passwords did not match"}

		stmt = "SELECT id FROM config WHERE k_username = %s"
		self._cursor.execute(stmt, [username])
		user_id = self._cursor.fetchone():
		if user_id:
			return {"error": "This username is already in use"}

		if not kroky_lib2.User(k_username, k_password):
			return {"error": "Username or password incorrect"}

		cherrypy.session["username"] = username
		cherrypy.session["id"] = user_id

		stmt = "INSERT INTO users (username, password) VALUES (%s, %s)"
		self._cursor.execute(stmt, [username, pbkdf2_sha256.hash(password)])
		self._db.commit()

		stmt = "INSERT INTO config (k_username, k_password) VALUES (%s, %s)"
		self._cursor.execute(stmt, [k_username, k_password])
		self._db.commit()

		raise cherrypy.HTTPRedirect("/")

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["GET"])
	@cherrypy.tools.require_auth()
	def get_order(self):
		stmt = "SELECT DATE_FORMAT(weekStart,'%d.%m.%Y'),DATE_FORMAT(weekEnd,'%d.%m.%Y'),DATE_FORMAT(updated_at,'%T %d.%m.%Y'),mon,tue,wed,thr,fri FROM log WHERE id = %s"
		self._cursor.execute(stmt, [cherrypy.session.get("id")])
		res = self._cursor.fetchone():

		if res:
			return {"weekStart": res[0], "weekEnd": res[1], "updated": res[2], "log": [res[3], res[4], res[5], res[6], res[7], res[8]]}
		return {}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["GET"])
	@cherrypy.tools.require_auth()
	def get_preferences(self):
		stmt = "SELECT conf_index, blacklist FROM config WHERE id = %s"
		self._cursor.execute(stmt, [cherrypy.session.get("id")])
		res = self._cursor.fetchone():

		if res:
			return {"index": res[0], "blacklist": res[1]}
		return {}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["GET"])
	@cherrypy.tools.require_auth()
	def get_preferences(self):
		stmt = "SELECT xxl, email, k_username FROM config WHERE id = %s"
		self._cursor.execute(stmt, [cherrypy.session.get("id")])
		res = self._cursor.fetchone():

		if res:
			return {"xxl": res[0], "email": res[1], "k_username": res[2]}
		return {}


if __name__ == '__main__':
	conf = {
	   '/': {
		   'tools.sessions.on': True,
		   'error_page.default': WebServer.error_page
		},
		'/public': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.abspath('../public')
		}
	}

	api = Api("", "", "")
	api.login = api.login

	cherrypy.tree.mount(WebServer(""), '/', conf)
	cherrypy.tree.mount(api, '/api', conf)
	cherrypy.server.socket_host = "127.0.0.1"
	cherrypy.engine.start()

