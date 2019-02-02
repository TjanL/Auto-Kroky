from kroky_lib2 import User
from database import Connector
from random import choice
import datetime
import argparse
import json
import os


class Order(object):

	class Item(object):
		def __init__(self, user, dan, meni, index, blacklist):
			self.ime = user.get_snack(dan, meni)
			self.meni = meni
			self.ocena = self._get_grade(index, blacklist)

		def _get_grade(self, index, blacklist):
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

	def __init__(self, single_user_id=None):
		parser = argparse.ArgumentParser()
		parser.add_argument("--user", type=int, nargs=1, help='ID of the user to order for')

		args = parser.parse_args()
		user_id = args.user[0] if args.user else single_user_id

		print("###############\n# Auto malica #\n###############")

		teden = ["pon", "tor", "sre", "cet", "pet"]
		meniji = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		log = {}

		with open("../settings.conf", "r") as f:
			settings = json.load(f)
			f.close()

		db = Connector(os.path.abspath("../database.db"))
		db.connect()
		results = db.get_config(user_id)

		for user in results:
			if user_id is None:
				user_id = user["id"]

			blacklist = json.loads(user["blacklist"])
			if blacklist is None:
				blacklist = []

			index = json.loads(user["conf_index"])
			if index is None:
				index = []
			index.reverse()

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

			monday = datetime.datetime.strptime(k.week, "%d.%m.%Y")
			friday = monday.date() + datetime.timedelta(days=4)
			print("-------------------|", monday.strftime("%d.%m.%Y"), "-", friday.strftime("%d.%m.%Y"), "|-------------------")

			for dan in range(len(teden)):
				# Get item grades
				item = [self.Item(k, dan, meni, index, blacklist) for meni in meniji]

				# Sort items by grade - first is the best choice
				item.sort(key=lambda x: (x.ocena), reverse=True)

				# Remove the best choice from item list and append it to choice list
				choice_list = []
				choice_list.append(item.pop(0))

				# Check if any other item has a same grade as best item or the item is "Day Canceled" (-1)
				for i in item:
					if i.ocena == choice_list[0].ocena or i.ocena == -1:
						choice_list.append(i)
					else: break

			# ------------------------------------------------------------------------------------------- #
				if choice_list[-1].ocena == -1:						# If last item is "False"
					print(teden[dan].capitalize(), ":", "Canceled")
					log[teden[dan]] = "Canceled"

				elif choice_list[0].ocena == 0:						# If the first item (best item) has grade 0
					if user["xxl"] and k.get_snack_xxl(dan, k.default_menu):
						k.set_snack_xxl(dan, k.default_menu)

					print(teden[dan].capitalize(), ":", "{} (Default menu)".format(k.get_snack(dan, k.default_menu)))
					log[teden[dan]] = "{} (Default menu)".format(k.get_snack(dan, k.default_menu))

				else:											# Randomly choose between best items
					item_choice = choice(choice_list)

					if user["xxl"] and k.get_snack_xxl(dan, item_choice.meni):
						k.set_snack_xxl(dan, item_choice.meni)
					else:
						k.set_snack(dan, item_choice.meni)

					print(teden[dan].capitalize(), ":", item_choice.ime)
					log[teden[dan]] = item_choice.ime
			# ------------------------------------------------------------------------------------------- #

			log = json.dumps(log, ensure_ascii=False)#.encode('utf8')
			db.set_log(user_id, monday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), log)

			if user["email"]:
				k.send_email()
				print("Email send!")

		db.close()


if __name__ == '__main__':
	Order()
