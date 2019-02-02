import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--remove", action='store_true', help='Remove crontab job.')

args = parser.parse_args()

dir_path = os.path.dirname(os.path.realpath(__file__))
python_path = sys.executable

cron_stmt = "0 12 * * 2 {} {}/lib/autokroky.py\n".format(python_path, dir_path)

if not args.remove:
	print("Installing cron job")
	print(cron_stmt)
	with open("/etc/cron.d/autokroky", "w") as file:
		file.write(cron_stmt)
		file.close()
else:
	os.remove("/etc/cron.d/autokroky")
	print("Removed cron job")
