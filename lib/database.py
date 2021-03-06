import sqlite3
import os


class Connector(object):
	def __init__(self, database):
		self.file_path = database
		if not os.path.isfile(database):
			self.connect()
			self._create_users_table()
			self._create_log_table()
			self._create_log_timestamp_triggers()
			self.close

	def connect(self):
		self._conn = sqlite3.connect(self.file_path)
		self._cursor = self._conn.cursor()

	def close(self):
		self._conn.close()

	def _create_users_table(self):
		stmt = """CREATE TABLE users (
				  'id' integer PRIMARY KEY AUTOINCREMENT,
				  'username' text NOT NULL,
				  'password' text NOT NULL,
				  'created_at' timestamp DEFAULT CURRENT_TIMESTAMP,
				  'xxl' integer NOT NULL DEFAULT '0',
				  'email' integer NOT NULL DEFAULT '0',
				  'k_username' text NOT NULL,
				  'k_password' text NOT NULL,
				  'blacklist' text DEFAULT '[]',
				  'conf_index' text DEFAULT '[]'
				);"""
		self._cursor.execute(stmt)
		self._conn.commit()

	def _create_log_table(self):
		stmt = """CREATE TABLE log (
				  'id' integer primary key autoincrement,
				  'user_id' integer NOT NULL UNIQUE,
				  'week_start' text,
				  'week_end' text,
				  'order_log' text DEFAULT '{}',
				  'updated_at' timestamp,
				  FOREIGN KEY(user_id) REFERENCES users(id)
				);"""
		self._cursor.execute(stmt)
		self._conn.commit()

	def _create_log_timestamp_triggers(self):
		stmt = """CREATE TRIGGER update_timestamp_INSERT AFTER INSERT ON log
					BEGIN
						UPDATE log SET updated_at = datetime('now') WHERE id = new.id;
					END;"""
		self._cursor.execute(stmt)

		stmt = """CREATE TRIGGER update_timestamp_UPDATE AFTER UPDATE ON log
					BEGIN
						UPDATE log SET updated_at = datetime('now') WHERE id = new.id;
					END;"""
		self._cursor.execute(stmt)
		self._conn.commit()

	def get_config(self, user_id=None):
		if user_id:
			stmt = "SELECT xxl,email,k_username,k_password,blacklist,conf_index FROM users WHERE id=?"
			self._cursor.execute(stmt, [user_id])
		else:
			stmt = "SELECT id, xxl, email, k_username, k_password, blacklist, conf_index FROM users"
			self._cursor.execute(stmt)

		columns = [col[0] for col in self._cursor.description]
		return [dict(zip(columns, row)) for row in self._cursor.fetchall()]

	def set_log(self, user_id, week_start, week_end, order_log):
		stmt = "UPDATE log SET week_start = ?, week_end = ?, order_log = ? WHERE user_id = ?"
		self._cursor.execute(stmt, [week_start, week_end, order_log, user_id])
		self._conn.commit()

	def get_login(self, username):
		stmt = "SELECT username, password, id FROM users WHERE username = ?"
		self._cursor.execute(stmt, [username])

		row = self._cursor.fetchone()
		if row:
			user, hash_pass, user_id = row
			return user, hash_pass, user_id
		return None

	def check_user(self, username):
		stmt = "SELECT id FROM users WHERE username = ?"
		self._cursor.execute(stmt, [username])
		user_id = self._cursor.fetchone()
		user_id = user_id[0] if user_id else None
		return user_id

	def check_k_user(self, username):
		stmt = "SELECT id FROM users WHERE k_username = ?"
		self._cursor.execute(stmt, [username])
		user_id = self._cursor.fetchone()
		user_id = user_id[0] if user_id else None
		return user_id

	def add_user(self, username, password, k_username, k_password):
		stmt = "INSERT INTO users (username, password, k_username, k_password) VALUES (?, ?, ?, ?)"
		self._cursor.execute(stmt, [username, password, k_username, k_password])
		self._conn.commit()

	def add_user_log(self, user_id):
		stmt = "INSERT INTO log (user_id) VALUES (?)"
		self._cursor.execute(stmt, [user_id])
		self._conn.commit()

	def get_log(self, user_id):
		stmt = "SELECT strftime('%d.%m.%Y',week_start),strftime('%d.%m.%Y',week_end),strftime('%H:%M:%S %d.%m.%Y', updated_at, 'localtime'),order_log FROM log WHERE user_id = ?"
		self._cursor.execute(stmt, [user_id])

		row = self._cursor.fetchone()
		if row:
			week_start, week_end, updated_at, order_log = row
			return week_start, week_end, updated_at, order_log
		return None

	def get_preferences(self, user_id):
		stmt = "SELECT conf_index, blacklist FROM users WHERE id = ?"
		self._cursor.execute(stmt, [user_id])

		row = self._cursor.fetchone()
		if row:
			conf_index, blacklist = row
			return conf_index, blacklist
		return None

	def get_profile(self, user_id):
		stmt = "SELECT xxl, email, k_username FROM users WHERE id = ?"
		self._cursor.execute(stmt, [user_id])

		row = self._cursor.fetchone()
		if row:
			xxl, email, k_username = row
			return xxl, email, k_username
		return None

	def set_preferences(self, user_id, index, blacklist):
		stmt = "UPDATE users SET conf_index=?, blacklist=? WHERE id = ?"
		self._cursor.execute(stmt, [index, blacklist, user_id])
		self._conn.commit()

	def set_profile(self, user_id, email, xxl, k_username=None, k_password=None):
		if k_username and k_password:
			stmt = "UPDATE users SET k_username=?, k_password=?, xxl=?, email=? WHERE id = ?";
			self._cursor.execute(stmt, [k_username, k_password, xxl, email, user_id])
		else:
			stmt = "UPDATE users SET xxl=?, email=? WHERE id = ?";
			self._cursor.execute(stmt, [xxl, email, user_id])
		self._conn.commit()
