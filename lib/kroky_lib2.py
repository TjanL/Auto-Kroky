import requests
from lxml import html


class User(object):
	"""basic commands for kroky.si"""
	def __init__(self, username, password):
		self._base_url = "http://www.kroky.si/2016/?mod=register"
		
		self._table_url = self._base_url + "&action=order"
		self._order_url = self._base_url + "&action=user2date2menu"

		self._session = requests.session()
		self._session.headers.update({
				"Origin":"http://www.kroky.si",
				"X-Requested-With":"XMLHttpRequest",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
				"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
				"Accept-Language":"en-US,en;q=0.9,sl;q=0.8"
			})
		
		if self._login(username, password):
			self._table_content = self._get_table_content()

			tmp_dict = self._get_profile_info()
			self.username = username
			self.name = tmp_dict["name"]
			self.surname = tmp_dict["surname"]
			self.default_menu = tmp_dict["default_menu"]
			self.week = tmp_dict["week"]

		self._meniji = {
			1: 3,
			2: 4,
			3: 5,
			4: 6,
			5: 7,
			6: 9,
			7: 10,
			8: 11,
			9: 12,
			10: 13,
			11: 15,
			12: 16,
			13: 18,
			14: 19
		}

	def _url_get(self, url, headers):
		response = self._session.get(url, headers=headers)
		if response.status_code == 200:
			response.encoding = "UTF-8"
			return html.fromstring(response.content)
		else:
			raise requests.ConnectionError("Site not reachable! Code: {0}".format(response.status_code))

	def _url_post(self, url, data, headers):
		response = self._session.post(url, data=data, headers=headers)
		if response.status_code != 200:
			raise requests.ConnectionError("Site not reachable! Code: {0}".format(response.status_code))
		return response.status_code

	def _login(self, username, password):
		url = self._base_url + "&action=login"
		self._url_post(url, data={"username": username, "password": password}, headers={"Referer": url})

		html_str = self._url_get(self._table_url, headers={"Referer": url})
		try:
			tmp = html_str.xpath("//table[@id='order_table']")[0]
		except:
			raise ValueError("Username or password incorrect!")
		return True

	def _get_table_content(self):
		url = self._base_url + "&action=login"
		html_str = self._url_get(self._table_url, headers={"Referer": url})
		return html_str.xpath("//table[@id='order_table']")[0]

	def _get_profile_info(self):
		url = self._base_url + "&action=editProfile"
		html_str = self._url_get(url, headers={"Referer": url})

		tmp_dict = {}
		tmp_dict["name"] = html_str.xpath("//body/div/form/table/tr[1]/td[2]")[0].text.strip()
		tmp_dict["surname"] = html_str.xpath("//body/div/form/table/tr[2]/td[2]")[0].text.strip()
		tmp_dict["default_menu"] = int(html_str.xpath("//body/div/form/table/tr[4]/td[2]/select/option[@selected]")[0].text.split()[1])
		tmp_dict["week"] = self._table_content.xpath("thead/tr/td[2]/span")[0].text.strip("(").strip(")")

		return tmp_dict

	def get_snack(self, day, menu):
		try:
			item = self._table_content.xpath("tr[{0!s}]/td[{1!s}]/label/span/span".format(self._meniji[menu], day + 2))

			return item[0].text
		except:
			return False

	def get_snack_xxl(self, day, menu):
		item = self._table_content.xpath("tr[{0!s}]/td[{1!s}]/div[@class='xl']|tr[{0!s}]/td[{1!s}]/div[@class='xxl']".format(self._meniji[menu], day + 2))

		if len(item) > 0:
			return True
		else:
			return False

	def set_snack(self, day, menu):
		item = self._table_content.xpath("tr[{0!s}]/td[{1!s}]/input".format(self._meniji[menu], day + 2))
		ID = item[0].get("cat_id")
		date = item[0].get("name")

		data = {"c": ID, "date": date}
		status_code = self._url_post(self._order_url, data=data, headers={"Referer": self._table_url})

		if status_code != 200:
			print("Could not select the item! {0!s}, {1!s}".format(day, menu))

	def set_snack_xxl(self, day, menu):
		item = self._table_content.xpath("tr[{0!s}]/td[{1!s}]/input".format(self._meniji[menu], day + 2))
		ID = item[0].get("cat_id")
		date = item[0].get("name")

		itemXXL = self._table_content.xpath("tr[{0!s}]/td[{1!s}]/div[@class='xl']|tr[{0!s}]/td[{1!s}]/div[@class='xxl']".format(self._meniji[menu], day + 2))
		if itemXXL[0].get("class") == "xl":
			xxl = "1"
		else:
			xxl = "2"

		data = {"c": ID, "date": date, "xl": xxl}
		status_code = self._url_post(self._order_url, data=data, headers={"Referer": self._table_url})
		
		if status_code != 200:
			print("Could not select the XXL! {0!s}, {1!s}".format(day, menu))

	def send_email(self):
		url = self._base_url + "&action=send_order_email"
		mon = self._table_content.xpath("thead/tr/td[2]/span")[0].text.strip("(").strip(")")
		sun = self._table_content.xpath("thead/tr/td[7]/span")[0].text.strip("(").strip(")")

		data = {"from": mon, "to": sun}
		status_code = self._url_post(url, data=data, headers={"Referer": url})
		
		if status_code != 200:
			print("Could not send email! {0}".format(status_code))
