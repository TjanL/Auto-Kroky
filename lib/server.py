from passlib.hash import pbkdf2_sha256
from datetime import datetime
from .kroky_lib2 import User
from .database import Connector
from .autokroky import Order
import cherrypy
import glob
import os
import json


class Root(object):
	def __init__(self, html_dir):
		# Preload html files to RAM
		self.html_dir = html_dir
		self.html_files = {}
		for file in glob.glob(os.path.join(self.html_dir, "*.html")):
			self.html_files[os.path.basename(file)] = open(file, encoding="utf8").read()

	@cherrypy.tools.register("before_handler")
	def require_site_auth():
		if cherrypy.session.get("username") is None:
			raise cherrypy.HTTPRedirect("/login")

	@cherrypy.expose
	@cherrypy.tools.require_site_auth()
	def index(self):
		return self.html_files["index.html"]

	@cherrypy.expose
	@cherrypy.tools.require_site_auth()
	def profile(self):
		return self.html_files["profile.html"]

	@cherrypy.expose
	@cherrypy.tools.require_site_auth()
	def preferences(self):
		return self.html_files["preferences.html"]

	@cherrypy.expose
	def login(self):
		return self.html_files["login.html"]

	@cherrypy.expose
	def register(self):
		return self.html_files["register.html"]

	@cherrypy.expose
	def logout(self):
		cherrypy.lib.sessions.expire()
		raise cherrypy.HTTPRedirect("/login")

	@cherrypy.expose
	def test(self):
		return open(os.path.join(self.html_dir, "test.html"), encoding="utf8").read()

	def error_page(self, status, message, traceback, version):
		return open(os.path.join(self.html_dir, "404.html"), encoding="utf8").read()


class Api(object):
	def __init__(self, db_file_path):
		self._db = Connector(db_file_path)

	def error_page(status, message, traceback, version):
		return status

	@cherrypy.tools.register("before_handler")
	def require_api_auth():
		if cherrypy.session.get("username") is None:
			raise cherrypy.HTTPError(401, "Unauthorized")

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["POST"])
	def login(self):
		input_json = cherrypy.request.json
		if input_json["username"] and input_json["password"]:
			self._db.connect()
			user = self._db.get_login(input_json["username"])
			self._db.close()
			if user:
				username, hash_pass, user_id = user
				if pbkdf2_sha256.verify(input_json["password"], hash_pass):
					cherrypy.session["username"] = username
					cherrypy.session["id"] = user_id
					return {"status": "Logged in"}
				else:
					return {"status": "Password incorrect"}
			else:
				return {"status": "Username not registered"}

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["POST"])
	def register(self):
		input_json = cherrypy.request.json
		self._db.connect()
		if input_json["username"]:
			if self._db.check_user(input_json["username"]):
				return {"status": "Username already taken"}

		if input_json["password"]:
			if len(input_json["password"]) < 6:
				return {"status": "Password must have atleast 6 characters"}
			elif input_json["c_password"] != input_json["password"]:
				return {"status": "Passwords do not match"}

		if input_json["k_username"] and input_json["k_password"]:
			if self._db.check_k_user(input_json["k_username"]):
				return {"status": "This username is already in use"}

			try:
				User(input_json["k_username"], input_json["k_password"])
			except ValueError:
				return {"status": "Username or password incorrect"}
		else:
			return None

		self._db.add_user(
			input_json["username"],
			pbkdf2_sha256.hash(input_json["password"]),
			input_json["k_username"],
			input_json["k_password"]
		)
		user_id = self._db.check_user(input_json["username"])
		self._db.add_user_log(user_id)
		self._db.close()

		cherrypy.session["username"] = input_json["username"]
		cherrypy.session["id"] = user_id

		return {"status": "Registered"}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.require_api_auth()
	@cherrypy.tools.allow(methods=["GET"])
	def get_order(self):
		self._db.connect()
		log = self._db.get_log(cherrypy.session.get("id"))
		self._db.close()
		if log:
			week_start, week_end, updated_at, order_log = log

			return {
				"weekStart": week_start,
				"weekEnd": week_end,
				"updated": updated_at,
				"log": json.loads(order_log)
			}
		return {}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.require_api_auth()
	@cherrypy.tools.allow(methods=["GET"])
	def get_preferences(self):
		self._db.connect()
		preferences = self._db.get_preferences(cherrypy.session.get("id"))
		self._db.close()
		if preferences:
			conf_index, blacklist = preferences
			conf_index = json.loads(conf_index) if conf_index else None
			blacklist = json.loads(blacklist) if blacklist else None
			return {
				"index": conf_index,
				"blacklist": blacklist
			}
		return {}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.require_api_auth()
	@cherrypy.tools.allow(methods=["GET"])
	def get_profile(self):
		self._db.connect()
		profile = self._db.get_profile(cherrypy.session.get("id"))
		self._db.close()
		if profile:
			xxl, email, k_username = profile
			return {
				"xxl": xxl,
				"email": email,
				"k_username": k_username
			}
		return {}

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.require_api_auth()
	@cherrypy.tools.allow(methods=["POST"])
	def update_preferences(self):
		input_json = cherrypy.request.json
		self._db.connect()
		self._db.set_preferences(cherrypy.session.get("id"),
								 json.dumps(input_json["levels"]),
								 json.dumps(input_json["blacklist"])
								)
		self._db.close()

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.require_api_auth()
	@cherrypy.tools.allow(methods=["POST"])
	def update_profile(self):
		input_json = cherrypy.request.json
		self._db.connect()

		if input_json["pass"]:
			try:
				User(input_json["user"], input_json["pass"])
			except ValueError:
				return {"status": "Username or password incorrect"}

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
								)
		self._db.close()

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.require_api_auth()
	@cherrypy.tools.allow(methods=["GET"])
	def get_user(self):
		return {"username": cherrypy.session.get("username")}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.require_api_auth()
	@cherrypy.tools.allow(methods=["POST"])
	def order(self):
		self._db.connect()
		log = self._db.get_log(cherrypy.session.get("id"))
		self._db.close()
		if log:
			_, _, time, _ = log
			now = datetime.now()
			last = datetime.strptime(time, "%H:%M:%S %d.%m.%Y")
			time_limit = 15 * 60 # 15 minutes

			time_delta = now - last
			if time_delta.total_seconds() >= time_limit:
				obj = Order(self._db.file_path, cherrypy.session.get("id"))
				del obj
			else:
				return {"status": time_limit - time_delta.total_seconds()}

		# No previous order
		obj = Order(self._db.file_path, cherrypy.session.get("id"))
		del obj

		return {}

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.allow(methods=["GET"])
	def test(self):
		self._db.connect()
		self._db.add_user("test", pbkdf2_sha256.hash("test"),"test", "test")

		user_id = self._db.check_user("test")
		cherrypy.session["username"] = "test"
		cherrypy.session["id"] = user_id
		self._db.add_user_log(user_id)

		log = {
		"pon": "Puranji zrezek v sirovi omaki, peteršiljev riž, napitek",
		"tor": "Sendvič s šunkarico in sirom, sadje, napitek",
		"sre": "Kremni piščančji ragu s krompirjevimi svaljki, napitek",
		"cet": "Sendvič s piščančjo poli salamo in sirom, sadje, napitek",
		"pet": "Testenine carbonaro s pečeno slanino in stepenimi jajci, napitek"
		}
		self._db.set_log(user_id, "2019-02-11", "2019-02-15", json.dumps(log, ensure_ascii=False))

		index = [
		["Puranji zrezek","Goveji stroganoff","skutni burek","skutni štruklji"],
		["Kus kus s tunino","Krompirjevi svaljki","Hot dog","Sadni cmoki","Svinjski zrezek"],
		["Cheeseburger","Pečena hrenovka v štručki s sirom","Piščančji dunajski zrezek"]
		]
		self._db.set_preferences(user_id, json.dumps(index, ensure_ascii=False), "[]")

		self._db.close()

		return {"username": "test", "password": "test", "index": index, "log": log}


if __name__ == '__main__':
	root_conf = {
	   '/': {
			'tools.sessions.on': True,
			'error_page.default': Root.error_page
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

	cherrypy.tree.mount(Root(os.path.abspath("../html")), '/', root_conf)
	cherrypy.tree.mount(Api(os.path.abspath("../database.db")), '/api', api_conf)
	cherrypy.server.socket_host = "127.0.0.1"
	cherrypy.engine.start()
