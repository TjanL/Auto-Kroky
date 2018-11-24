import MySQLdb


class Connect(object):
	def __init__(self, user, password, database, ip="localhost"):
		self._db = MySQLdb.connect(ip, user, password, database, charset='utf8')
		self._cursor = self._db.cursor()

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
		self._db.commit()

	def close(self):
		self._db.close()
