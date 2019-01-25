import sqlite3


class Connector(object):
	def __init__(self, database):
		self._db_name = database

	def connect(self):
		self._conn = sqlite3.connect(self._db_name)
		self._cursor = self._conn.cursor()

	def close(self):
		self._conn.close()

	def get_config(self, user_id=None):
		if user_id:
			stmt = "SELECT xxl,email,k_username,k_password,blacklist,conf_index FROM config WHERE id=%s"
			self._cursor.execute(stmt, [user_id])
		else:
			stmt = "SELECT id, xxl, email, k_username, k_password, blacklist, conf_index FROM config"
			self._cursor.execute(stmt)

		columns = [col[0] for col in self._cursor.description]
		return [dict(zip(columns, row)) for row in self._cursor.fetchall()]

	def set_log(self, user_id, week_start, week_end, order_log):
		stmt = "INSERT INTO log (id, week_start, week_end, order_log) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE week_start=%s, week_end=%s, order_log=%s"
		self._cursor.execute(stmt, (user_id, week_start, week_end, order_log, week_start, week_end, order_log))
		self._conn.commit()

	def get_login(self, username):
		stmt = "SELECT username, password, id FROM users WHERE username = %s"
		self._cursor.execute(stmt, [username])
		user, hash_pass, user_id = cursor.fetchone()

		return user, hash_pass, user_id

	def check_user(self, username):
		stmt = "SELECT id FROM users WHERE username = %s"
		self._cursor.execute(stmt, [username])
		user_id = self._cursor.fetchone()
		return user_id

	def check_k_user(self, username):
		stmt = "SELECT id FROM config WHERE k_username = %s"
		self._cursor.execute(stmt, [username])
		user_id = self._cursor.fetchone()
		return user_id

	def add_user(self, username, password):
		stmt = "INSERT INTO users (username, password) VALUES (%s, %s)"
		self._cursor.execute(stmt, [username, password])
		self._conn.commit()

	def add_user_config(self, k_username, k_password):
		stmt = "INSERT INTO config (k_username, k_password) VALUES (%s, %s)"
		self._cursor.execute(stmt, [k_username, k_password])
		self._conn.commit()

	def get_log(self, user_id):
		stmt = "SELECT DATE_FORMAT(week_start,'%d.%m.%Y'),DATE_FORMAT(week_end,'%d.%m.%Y'),DATE_FORMAT(updated_at,'%T %d.%m.%Y'),order_log FROM log WHERE id = ?"
		self._cursor.execute(stmt, [user_id])
		week_start, week_end, updated_at, order_log = self._cursor.fetchone()
		return week_start, week_end, updated_at, order_log

	def get_preferences(self, user_id):
		stmt = "SELECT conf_index, blacklist FROM config WHERE id = ?"
		self._cursor.execute(stmt, [user_id])
		conf_index, blacklist = self._cursor.fetchone()
		return conf_index, blacklist

	def get_profile(self, user_id):
		stmt = "SELECT xxl, email, k_username FROM config WHERE id = ?"
		self._cursor.execute(stmt, [user_id])
		xxl, email, k_username = self._cursor.fetchone()
		return xxl, email, k_username

	def set_preferences(self, user_id, index, blacklist):
		stmt = "UPDATE config SET conf_index=?, blacklist=? WHERE id = ?"
		self._cursor.execute(stmt, (index, blacklist, user_id))
		self._conn.commit()

	def set_profile(self, user_id, email, xxl, k_username, k_password=None):
		if k_password:
			stmt = "UPDATE config SET k_username=?, k_password=?, xxl=?, email=? WHERE id = ?";
			self._cursor.execute(stmt, (k_username, k_password, xxl, email, user_id))
		else:
			stmt = "UPDATE config SET k_username=?, xxl=?, email=? WHERE id = ?";
			self._cursor.execute(stmt, (k_username, xxl, email, user_id))
		self._conn.commit()
