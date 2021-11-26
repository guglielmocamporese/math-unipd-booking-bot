"""
This project creates an API for accessing and interacting with the booking system at the math department at unipd.
Written by Guglielmo Camporese, guglielmocamporese@gmail.com
"""

import argparse
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

CHROME_DRIVER_PATH = './chromedriver' # path of chromedriver

def load_page(user, pwd):
	"""
	Load the booking web-page given the math.unipd credentials.
	"""
	# Load page

	op = webdriver.ChromeOptions()
	op.add_argument('headless')
	driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=op)
	driver.get(f'https://{user}:{pwd}@novnc.math.unipd.it/presenze/index.php')
	return driver

def get_args(stdin):
	"""
	Parse input arguments.
	"""
	now = datetime.datetime.now()
	parser = argparse.ArgumentParser(stdin)
	parser.add_argument('--mode', type=str, default='book', help='Year of the booking.', choices=['book', 'check', 'remove'])
	parser.add_argument('--year', '-y', type=int, default=now.year, 
						help='Year of the booking.', choices=[2020, 2021, 2022])
	parser.add_argument('--month', '-m', type=int, default=now.month, 
						help='Month number of the booking.', choices=list(range(1, 13)))
	parser.add_argument('--day', '-d', type=int, default=now.day, help='Day of the booking.')
	parser.add_argument('--arrival', '-ta', type=int, default=9, 
						help='Time of arrival (h) of the booking.', choices=list(range(7, 19)))
	parser.add_argument('--departure', '-td', type=int, default=18, 
						help='Time of departure (h) of the booking.', choices=list(range(8, 20)))
	parser.add_argument('--office', '-o', type=int, default=732, help='Office number.')
	parser.add_argument('--guests', '-g', type=str, default='', help='Guests names (optional).')

	parser.add_argument('--today', action='store_true', help='Use today as the time reference.')
	parser.add_argument('--tomorrow', action='store_true', help='Use tomorrow as the time reference.')
	parser.add_argument('--this_week', action='store_true', help='Use this week as the time reference.')
	parser.add_argument('--next_week', action='store_true', help='Use next week as the time reference.')
	parser.add_argument('--this_month', action='store_true', help='Use this month as the time reference.')
	parser.add_argument('--next_month', action='store_true', help='Use next month as the time reference.')
	args = vars(parser.parse_args())

	# Process input args
	if args['today']:
		args['year'], args['month'], args['day'] = now.year, now.month, now.day
	if args['tomorrow']:
		args['year'], args['month'], args['day'] = now.year, now.month, now.day + 1
	args['month'] = datetime.date(1900, args['month'] , 1).strftime('%B') # int to string
	return args