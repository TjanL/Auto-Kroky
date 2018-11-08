import requests
from lxml import html

class kroky(object):
	"""basic commands for kroky.si"""
	def __init__(self, username, password, verbose=False):
		baseUrl = "http://www.kroky.si/2016/?mod=register"
		loginUrl = baseUrl + "&action=login"
		self._tableUrl = baseUrl + "&action=order"
		self._orderUrl = baseUrl + "&action=user2date2menu"
		self._emailUrl = baseUrl + "&action=send_order_email"
		self._profileUrl = baseUrl + "&action=editProfile"

		self.username = username

		self._session = requests.session()

		self._session.headers.update({
				"Origin":"http://www.kroky.si",
				"X-Requested-With":"XMLHttpRequest",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
				"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
				"Accept-Language":"en-US,en;q=0.9,sl;q=0.8"
			})

		if verbose: print("Loging in")

		response = self._session.post(loginUrl, data={"username":username,"password":password}, headers={"Referer": loginUrl})
		
		if response.status_code == 200:

			html_content = self._session.get(self._tableUrl, headers={"Referer": loginUrl})
			html_content.encoding = "UTF-8"

			html_content = html.fromstring(html_content.content)

			try:
				self.table_content = html_content.xpath("//table[@id='order_table']")[0]
			except:
				raise ValueError("Username or password incorrect!")

			if verbose: print("Logged-in as {0}".format(username))


			html_content = self._session.get(self._profileUrl, headers={"Referer": self._profileUrl})
			html_content.encoding = "UTF-8"

			html_content = html.fromstring(html_content.content)

			self.name = html_content.xpath("//body/div/form/table/tr[1]/td[2]")[0].text.strip()
			self.surname = html_content.xpath("//body/div/form/table/tr[2]/td[2]")[0].text.strip()

			self.defaultMenu = int(html_content.xpath("//body/div/form/table/tr[4]/td[2]/select/option[@selected]")[0].text.split()[1])

			self.firstWeekDate = self.table_content.xpath("thead/tr/td[2]/span")[0].text.strip("(").strip(")")
			self.lastWeekDate = self.table_content.xpath("thead/tr/td[6]/span")[0].text.strip("(").strip(")")

		else:
			raise ValueError("Site not reachable! Code: {0}".format(response.status_code))

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

	def checkItem(self, day, menu):
		try:
			item = self.table_content.xpath("tr[{0!s}]/td[{1!s}]/label/span/span".format(self._meniji[menu], day + 2))

			return item[0].text
		except:
			return False

	def checkXXL(self, day, menu):
		item = self.table_content.xpath("tr[{0!s}]/td[{1!s}]/div[@class='xl']|tr[{0!s}]/td[{1!s}]/div[@class='xxl']".format(self._meniji[menu], day + 2))

		if len(item) > 0:
			return True
		else:
			return False

	def selectItem(self, day, menu):
		item = self.table_content.xpath("tr[{0!s}]/td[{1!s}]/input".format(self._meniji[menu], day + 2))
		ID = item[0].get("cat_id")
		date = item[0].get("name")

		data = {"c": ID, "date": date}
		response = self._session.post(self._orderUrl, data=data, headers={"Referer": self._tableUrl})

		if response.status_code != 200:
			print("Could not select the item! {0!s}, {1!s}".format(day, menu))

	def selectXXL(self, day, menu):
		item = self.table_content.xpath("tr[{0!s}]/td[{1!s}]/input".format(self._meniji[menu], day + 2))
		ID = item[0].get("cat_id")
		date = item[0].get("name")

		itemXXL = self.table_content.xpath("tr[{0!s}]/td[{1!s}]/div[@class='xl']|tr[{0!s}]/td[{1!s}]/div[@class='xxl']".format(self._meniji[menu], day + 2))
		if itemXXL[0].get("class") == "xl":
			xxl = "1"
		else:
			xxl = "2"

		data = {"c": ID, "date": date, "xl": xxl}
		response = self._session.post(self._orderUrl, data=data, headers={"Referer": self._tableUrl})
		
		if response.status_code != 200:
			print("Could not select the XXL! {0!s}, {1!s}".format(day, menu))

	def sendEmail(self):
		mon = self.table_content.xpath("thead/tr/td[2]/span")[0].text.strip("(").strip(")")
		sun = self.table_content.xpath("thead/tr/td[7]/span")[0].text.strip("(").strip(")")

		data = {"from": mon, "to": sun}
		response = self._session.post(self._emailUrl, data=data, headers={"Referer": self._emailUrl})
		
		if response.status_code != 200:
			print("Could not send email! {0}".format(response.status_code))