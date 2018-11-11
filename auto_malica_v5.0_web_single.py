# Tjan Ljubesek #
# April 2018    #
import kroky_lib2, MySQLdb, argparse, json
from random import choice

print("###############\n# Auto malica #\n###############")

db = MySQLdb.connect("localhost","","","autoMalica",charset='utf8')

cursor = db.cursor()

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("userID", metavar="I", type=int, nargs=1, help='User ID')

args = parser.parse_args()

usr_id = args.userID

stmt = "SELECT xxl,email,k_username,k_password,blacklist,conf_index FROM config where id=%s"
cursor.execute(stmt, (usr_id))
user = cursor.fetchone()

xxl = user[0]
email = user[1]
username = user[2]
password = user[3]

blacklist = json.loads(user[4])
if blacklist is None:
	blacklist = []
index = json.loads(user[5])
if index is None:
	blacklist = []
index.reverse()


print("\n"+username)
if not index:
	print("No index, skipping...")
	db.close()
	raise SystemExit
try:
	# Initialize
	k = kroky_lib2.kroky(username, password,verbose=True)
except Exception as e:
	print("Username or password incorrect!")
	db.close()
	raise SystemExit


print("-------------------|",k.firstWeekDate,"-",k.lastWeekDate,"|-------------------")

teden = ["pon", "tor", "sre", "cet", "pet"]
meniji = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
log = {"pon":"", "tor":"", "sre":"", "cet":"", "pet":""}

for dan in range(len(teden)):

	# Reset items and choice list
	#	grade,name,menu
	item = [[0,"",""] for i in range(len(meniji))]
	choiceList = []

	# Get item grade by searching index words in it
	itemNumber = 0
	for meni in meniji:
		grade = 0
		item[itemNumber][1] = k.checkItem(dan, meni)
		item[itemNumber][2] = meni

		if item[itemNumber][1] == False: # If "False", day is canceled
			item[itemNumber][0] = -1
		else:
			skip = False
			for block in blacklist:
				if block.lower() in item[itemNumber][1].lower(): # Check if string contains any blacklisted words
					item[itemNumber][0] = 0
					skip = True
					break
			if not skip:
				for y in index:
					grade += 1
					for x in y:
						if x.lower() in item[itemNumber][1].lower():
							item[itemNumber][0] = grade
							break
		itemNumber += 1


	# Sort items by grade - first is the best choice
	item.sort(key=lambda x: (x[0]), reverse=True)

	# Remove the best choice from item list and append it to choice list
	choiceList.append(item.pop(0))

	# Check if any other item has a same grade as best item or the item is "Day Canceled" (-1)
	for i in item:
		if i[0] == choiceList[0][0] or i[0] == -1:
			choiceList.append(i)
		else: break


	if choiceList[-1][0] == -1:						# If last item is "False"
		print(teden[dan].capitalize(),":","Canceled")
		log[teden[dan]] = "Canceled"

	elif choiceList[0][0] == 0:						# If the first item (best item) has grade 0
		if xxl and k.checkXXL(dan, k.defaultMenu):
			k.selectXXL(dan, k.defaultMenu)

		print(teden[dan].capitalize(),":","{} (Default menu)".format(k.checkItem(dan, k.defaultMenu)))
		log[teden[dan]] = "{} (Default menu)".format(k.checkItem(dan, k.defaultMenu))

	else:											# Randomly choose between best items
		itemChoice = choice(choiceList)

		if xxl and k.checkXXL(dan, itemChoice[2]):
			k.selectXXL(dan, itemChoice[2])
		else:
			k.selectItem(dan, itemChoice[2])

		print(teden[dan].capitalize(),":",itemChoice[1])
		log[teden[dan]] = itemChoice[1]


	tmp = k.firstWeekDate.split(".")
	weekStart = tmp[2]+"-"+tmp[1]+"-"+tmp[0]
	tmp = k.lastWeekDate.split(".")
	weekEnd = tmp[2]+"-"+tmp[1]+"-"+tmp[0]

log = json.dumps(log, ensure_ascii=False).encode('utf8')
stmt = "INSERT INTO log (id, weekStart, weekEnd, order_log) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE weekStart=%s, weekEnd=%s, order_log=%s"
cursor.execute(stmt, (usr_id, weekStart, weekEnd, log, weekStart, weekEnd, log))
db.commit()

if email:
	k.sendEmail()
	print("Email send!")

db.close()