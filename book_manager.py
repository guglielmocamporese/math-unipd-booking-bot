"""
This project creates an API for accessing and interacting with the booking system at the math department at unipd.
Written by Guglielmo Camporese, guglielmocamporese@gmail.com
"""

import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import load_page

HTML_FORM_IDS = {
    'year': 'tyear',
    'month': 'tmonth',
    'day': 'tday',
    'arrival': 'tbegin',
    'departure': 'tend',
    'office': 'tufficio',
    'guests': 'tguest',
}
VERBOSE = True

def book_single_day(user, pwd, args):
    """
    Book the office on a single day.
    """
    driver = load_page(user, pwd)
    for k in ['year', 'month', 'day']:
        search = driver.find_elements(By.NAME, HTML_FORM_IDS[k])[0]
        search.send_keys(args[k])
    search.send_keys(Keys.RETURN)

    search = driver.find_elements(By.TAG_NAME, 'table')[0]
    search = search.find_elements(By.TAG_NAME, 'tr')
    reservation_already_done = len(search) > 1

    if reservation_already_done:
        h0, h1, _, office = search[1].text.split()
        day_str = datetime.datetime(args['year'], datetime.datetime.strptime(args['month'], '%B').month, 
                                                                                args['day']).strftime('%a')
        print(f'You have already booked the office {office} for {day_str} {args["day"]}-{args["month"][:3]}-{args["year"]} '
                  f'from {int(h0)}:00 to {int(h1)}:00.')
    
    else:
        for k in ['arrival', 'departure', 'office', 'guests']:
            search = driver.find_elements(By.NAME, HTML_FORM_IDS[k])[0]
            search.send_keys(args[k])
        search.send_keys(Keys.RETURN)

        search = driver.find_elements(By.CLASS_NAME, 'sansserif')
        reservation_done = not any(['Access not permitted' in s.text for s in search]) 
        if VERBOSE:
            if reservation_done:
                day_str = datetime.datetime(args['year'], datetime.datetime.strptime(args['month'], '%B').month, 
                                                                        args['day']).strftime('%a')
                print(f'Reservation on {day_str} {args["day"]}-{args["month"][:3]}-{args["year"]} ' 
                          f'from {args["arrival"]}:00 to {args["departure"]}:00 in the office {args["office"]} done!')
            else:
                print('Reservation not done.')
    driver.quit()

def check_single_day(user, pwd, args):
    """
    Book the office on a single day.
    """
    driver = load_page(user, pwd)
    for k in ['year', 'month', 'day']:
        search = driver.find_elements(By.NAME, HTML_FORM_IDS[k])[0]
        search.send_keys(args[k])
    search.send_keys(Keys.RETURN)

    search = driver.find_elements(By.TAG_NAME, 'table')[0]
    search = search.find_elements(By.TAG_NAME, 'tr')
    reservation_already_done = len(search) > 1
    day_str = datetime.datetime(args['year'], datetime.datetime.strptime(args['month'], '%B').month, 
                                                            args['day']).strftime('%a')
    if reservation_already_done:
        h0, h1, _, office = search[1].text.split()
        print(f'You have already booked the office {office} for {day_str} {args["day"]}-{args["month"][:3]}-{args["year"]} '
                  f'from {int(h0)}:00 to {int(h1)}:00.')
    else:
        print(f'You have NOT booked the office {args["office"]} for {day_str} {args["day"]}-{args["month"][:3]}-{args["year"]}.')
    driver.quit()

def remove_single_day(user, pwd, args):
    """
    Remove booking on a single day.
    """
    driver = load_page(user, pwd)
    for k in ['year', 'month', 'day']:
        search = driver.find_elements(By.NAME, HTML_FORM_IDS[k])[0]
        search.send_keys(args[k])
    search.send_keys(Keys.RETURN)

    search = driver.find_elements(By.TAG_NAME, 'table')[0]
    search = search.find_elements(By.TAG_NAME, 'tr')
    reservation_already_done = len(search) > 1
    day_str = datetime.datetime(args['year'], datetime.datetime.strptime(args['month'], '%B').month, 
                                                            args['day']).strftime('%a')
    if reservation_already_done:
        search = driver.find_elements(By.ID, 'chooseday')[0]
        search.click()
        search = driver.find_elements(By.CLASS_NAME, 'sansserif')
        removed = any(['Delete successful' in s.text for s in search])
        if removed:
            print(f'Booking in office {args["office"]} for {day_str} {args["day"]}-{args["month"][:3]}-{args["year"]} removed.')
        else:
            print(f'Booking in office {args["office"]} for {day_str} {args["day"]}-{args["month"][:3]}-{args["year"]} NOT removed.')
    else:
        print(f'You have NOT booked the office {args["office"]} for {day_str} {args["day"]}-{args["month"][:3]}-{args["year"]}.')
    driver.quit()

class BookManager:
    def __init__(self, user, pwd, args, mode=None):
        self.user = user
        self.pwd = pwd
        self.args = args
        assert mode in ['book', 'check', 'remove']
        self.mode = mode

    def run(self):
        """
        Run the book manager (book reservations, check reservations, remove ressrvations).
        """
        days = [datetime.date.today()]
        if self.args['this_week']:
            day = days[-1] + datetime.timedelta(1)
            while True:
                if day.strftime('%a') in ['Sat', 'Sun']:
                    break
                days += [day]
                day += datetime.timedelta(1)
        
        elif self.args['next_week']:
            day = days[-1] + datetime.timedelta(1)
            weekend_passed = False
            while True:
                if day.strftime('%a') not in ['Sat', 'Sun']:
                    days += [day]
                elif day.strftime('%a') == 'Sat':
                    if weekend_passed:
                            break
                elif day.strftime('%a') == 'Sun':
                    weekend_passed = True
                day += datetime.timedelta(1)

        elif self.args['this_month']:
            day = days[-1] + datetime.timedelta(1)
            year, month = datetime.date.today().year, datetime.date.today().month
            while True:
                if (day.year * 12 + day.month - (year * 12 + month)) == 1:
                    break
                if day.strftime('%a') not in ['Sat', 'Sun']:
                    days += [day]
                day += datetime.timedelta(1)

        elif self.args['next_month']:
            day = days[-1] + datetime.timedelta(1)
            year, month = datetime.date.today().year, datetime.date.today().month
            while True:
                if (day.year * 12 + day.month - (year * 12 + month)) == 2:
                    break
                if day.strftime('%a') not in ['Sat', 'Sun']:
                    days += [day]
                day += datetime.timedelta(1)

        else:
            if self.mode == 'book':
                return book_single_day(self.user, self.pwd, self.args)
            elif self.mode == 'check':
                return check_single_day(self.user, self.pwd, self.args)
            elif self.mode == 'remove':
                return remove_single_day(self.user, self.pwd, self.args)

        out = []
        for day in days:
            args_day = self.args
            args_day['year'], args_day['month'], args_day['day'] = day.year, day.month, day.day
            args_day['month'] = datetime.date(1900, args['month'] , 1).strftime('%B')
            if self.mode == 'book':
                out_i = book_single_day(self.user, self.pwd, args_day)
            elif self.mode == 'check':
                out_i = check_single_day(self.user, self.pwd, args_day)
            elif self.mode == 'remove':
                out_i = remove_single_day(self.user, self.pwd, args_day)
            out += [out_i]
        return out


if __name__ == '__main__':
    import sys
    import getpass
    from utils import get_args

    # Retrieve input args
    args = get_args(sys.argv[1:])

    # Retrieve math credentials
    user = input('[Username] ') if len(args['user']) == 0 else args['user']
    pwd = getpass.getpass('[Password] ') if len(args['pwd']) == 0 else args['pwd']
    

    # Book
    bm = BookManager(user, pwd, args, mode=args['mode'])
    bm.run()
