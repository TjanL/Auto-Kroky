from subprocess import call
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
python_path = sys.executable

cron_stmt = "0 12 * * 2 {} {}/lib/autokroky.py".format(python_path, dir_path)

with open("cron_job", "w") as file:
	file.write(cron_stmt)
	file.close()

print("Installing cron job")
print(cron_job)
call(["crontab", os.abspath("cron_job")])

os.remove(os.abspath("cron_job"))
