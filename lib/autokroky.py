from .kroky_lib2 import User
from .database import Connector
from random import choice
import datetime
import json


class Order():

	teden = ["pon", "tor", "sre", "cet", "pet"]
	meniji = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

	class Item(object):
		def __init__(self, user, dan, meni, index, blacklist):
			self.ime = user.get_snack(dan, meni)
			self.meni = meni
			self.ocena = self.get_grade(reversed(index), blacklist)

		def get_grade(self, index, blacklist):
			if self.ime != False: # If "False", day is canceled
				tmp = 0
				for block in blacklist:
					if block.lower() in self.ime.lower(): # Check if string contains any blacklisted words
						return tmp

				grade = 0
				for y in index:
					grade += 1
					for x in y:
						if x.lower() in self.ime.lower():
							tmp = grade
							break
				return tmp
			return -1

	def get_blacklist(user_config):
		blacklist = json.loads(user_config["blacklist"])
		if blacklist is None:
			blacklist = []
		return blacklist

	def get_index(user_config):
		index = json.loads(user_config["conf_index"])
		if index is None:
			index = []
		return index

	def order_item(k_user, user_config, dan, choice_list):
		if choice_list[-1].ocena == -1:						# If last item is "False"
			return "Canceled"

		elif choice_list[0].ocena == 0:						# If the first item (best item) has grade 0
			if user_config["xxl"] and k_user.get_snack_xxl(dan, k_user.default_menu):
				k_user.set_snack_xxl(dan, k_user.default_menu)

			return "{} (Default menu)".format(k_user.get_snack(dan, k_user.default_menu))

		else:											# Randomly choose between best items
			item_choice = choice(choice_list)

			if user_config["xxl"] and k_user.get_snack_xxl(dan, item_choice.meni):
				k_user.set_snack_xxl(dan, item_choice.meni)
			else:
				k_user.set_snack(dan, item_choice.meni)

			return item_choice.ime

	def run(database, user_id=None):
		db = Connector(database)
		db.connect()
		results = db.get_config(user_id)

		for user in results:
			blacklist = Order.get_blacklist(user)
			index = Order.get_index(user)

			print("\n"+user["k_username"])
			if not index:
				print("No index, skipping...")
				continue
			try:
				# Initialize
				k = User(user["k_username"], user["k_password"])
			except Exception as e:
				print(e)
				continue

			log = {}
			for dan in range(len(Order.teden)):
				# Get item grades
				item = [Order.Item(k, dan, meni, index, blacklist) for meni in Order.meniji]

				# Sort items by grade - first is the best choice
				item.sort(key=lambda x: (x.ocena), reverse=True)

				# Remove the best choice from item list and append it to choice list
				choice_list = []
				choice_list.append(item.pop(0))

				# Check if any other item has a same grade as best item or the item is "Day Canceled" (-1)
				for i in item:
					if i.ocena == choice_list[0].ocena or i.ocena == -1:
						choice_list.append(i)
					else:
						break

				log[Order.teden[dan]] = Order.order_item(k, user, dan, choice_list)

			log = json.dumps(log, ensure_ascii=False)#.encode('utf8')
			monday = datetime.datetime.strptime(k.week, "%d.%m.%Y")
			friday = monday.date() + datetime.timedelta(days=4)
			db.set_log(user["id"], monday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), log)

			if user["email"]:
				k.send_email()
				print("Email send!")

			print("Done")

		db.close()



if __name__ == '__main__':
	Order().run()
