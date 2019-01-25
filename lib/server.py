from passlib.hash import pbkdf2_sha256
import kroky_lib2
import cherrypy
import glob
import os
import database


class WebServer(object):
	def __init__(self):
		# Preload html files
		self.html_files = {}
		for file in glob.glob(os.path.abspath("../html/*.html")):
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

	@cherrypy.expose
	def test(self):
		return open(os.path.abspath("../html/test.html"), encoding="utf8").read()

	def error_page(status, message, traceback, version):
		return open(os.path.abspath("../html/404.html"), encoding="utf8").read()


class Api(object):
	def __init__(self, db_file_path):
		self._db = database.Connector(db_file_path)

	def error_page(status, message, traceback, version):
		return status

	@cherrypy.tools.register("before_handler")
	def require_auth():
		if not cherrypy.session.get("id"):
			return {"error": "Not logged in!"}

	@cherrypy.tools.register("before_handler")
	def db_connect(self):
		self._db.connect()

	@cherrypy.tools.register("on_end_request")
	def db_disconnect(self):
		self._db.close()

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.db_connect()
	@cherrypy.tools.db_disconnect()
	@cherrypy.tools.allow(methods=["GET"])
	def login(self, username, password):
		if username and password:
			username, hash_pass, user_id = self._db.get_login(username)
			if pbkdf2_sha256.verify(password, hash_pass):
				cherrypy.session["username"] = username
				cherrypy.session["id"] = user_id
				raise cherrypy.HTTPRedirect("/")

		return {"error": "Username or password incorrect!"}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.db_connect()
	@cherrypy.tools.db_disconnect()
	@cherrypy.tools.allow(methods=["GET"])
	def register(self, username, password, c_password, k_username, k_password):
		if username:
			if self._db.check_user(username):
				return {"error": "Username already taken!"}

		elif password:
			if len(password) < 6:
				return {"error": "Password must have atleast 6 characters"}
			elif c_password != password:
				return {"error": "Passwords did not match"}

		if self._db.check_k_user(k_username):
			return {"error": "This username is already in use"}

		if not kroky_lib2.User(k_username, k_password):
			return {"error": "Username or password incorrect"}

		cherrypy.session["username"] = username
		cherrypy.session["id"] = user_id

		self._db.add_user(username, pbkdf2_sha256.hash(password))
		self._db.add_user_config(k_username, k_password)

		raise cherrypy.HTTPRedirect("/")

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.db_connect()
	@cherrypy.tools.db_disconnect()
	@cherrypy.tools.require_auth()
	@cherrypy.tools.allow(methods=["GET"])
	def get_order(self):
		week_start, week_end, updated_at, order_log = self._db.get_log(cherrypy.session.get("id"))
		if week_start and week_end and updated_at and order_log:
			return {
				"weekStart": week_start,
				"weekEnd": weekEnd,
				"updated": updated_at,
				"log": order_log
			}
		return {}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.db_connect()
	@cherrypy.tools.db_disconnect()
	@cherrypy.tools.require_auth()
	@cherrypy.tools.allow(methods=["GET"])
	def get_preferences(self):
		conf_index, blacklist = self._db.get_preferences(cherrypy.session.get("id"))
		if conf_index and blacklist:
			return {
				"index": conf_index,
				"blacklist": blacklist
			}
		return {}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.db_connect()
	@cherrypy.tools.db_disconnect()
	@cherrypy.tools.require_auth()
	@cherrypy.tools.allow(methods=["GET"])
	def get_profile(self):
		xxl, email, k_username = self._db.get_profile(cherrypy.session.get("id"))
		if xxl and email and k_username:
			return {
				"xxl": xxl,
				"email": email,
				"k_username": k_username
			}
		return {}

	#@cherrypy.tools.db_connect()
	#@cherrypy.tools.db_disconnect()
	#@cherrypy.tools.require_auth()
	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["POST"])
	def update_preferences(self):
		input_json = cherrypy.request.json
		self._db.set_preferences(cherrypy.session.get("id"),
								 input_json["levels"],
								 input_json["blacklist"]
								)

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["POST"])
	def update_profile(self):
		input_json = cherrypy.request.json
		if input_json["pass"]:
			if not kroky_lib2.User(input_json["user"], input_json["pass"]):
				return {"error": "Username or password incorrect"}

			self._db.set_profile(cherrypy.session.get("id"),
								 input_json["email"],
								 input_json["xxl"],
								 input_json["user"],
								 input_json["pass"]
								)
		else:
			self._db.set_profile(cherrypy.session.get("id"),
								 input_json["email"],
								 input_json["xxl"],
								 input_json["user"]
								)

	def run_auto_kroky(self):
		input_json = cherrypy.request.json


	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["POST"])
	def test(self):
		print(cherrypy.request.json)


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

	api_conf = {
		'/': {
			   'tools.sessions.on': True,
			   'error_page.default': Api.error_page
			}
	}

	api = Api("")
	api.login = api.login

	cherrypy.tree.mount(WebServer(), '/', conf)
	cherrypy.tree.mount(api, '/api', api_conf)
	cherrypy.server.socket_host = "127.0.0.1"
	cherrypy.engine.start()
