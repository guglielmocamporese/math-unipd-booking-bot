import requests
from requests.auth import HTTPBasicAuth
from lxml import etree
import re
import datetime
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='<code>%(message)s</code>')

class BookManager:
    """
    Book manager definition.
    """
    def __init__(self, user, pwd, verbose=True):
        self.user = user
        self.pwd = pwd
        self.verbose = verbose
        
    def book_single(self, args, verbose=None):
        """
        Book for a single timeslot.
        """
        if verbose is None:
            verbose = self.verbose
        with requests.Session() as s:
            payload = {
                'tday': f'{args.day:02d}',
                'tmonth': f'{args.month:02d}',
                'tyear': f'{args.year}',
                'tbegin': f'{args.arrival:02d}',
                'tend': f'{args.departure:02d}',
                'tufficio': f'{args.office}',
                'tguest': f'{args.guests}',
            }
            r = s.post('https://novnc.math.unipd.it/presenze/time.php', auth=HTTPBasicAuth(self.user, self.pwd), 
                       data=payload)
            r = s.post('https://novnc.math.unipd.it/presenze/register.php', auth=HTTPBasicAuth(self.user, self.pwd), 
                       data=payload)
        booked = 'Access not permitted' not in r.text 
        if booked:
            logging.info(f'Registration for {args.day_str[:3]} {args.year}-{args.month}-{args.day} in the office '
                         f'{args.office} done!')
        else:
            logging.info(f'Registration for {args.day_str[:3]} {args.year}-{args.month}-{args.day} in the office '
                         f'{args.office} already done!')
        return booked

    def check_single(self, args, verbose=None):
        """
        Check a booking given a specific day.
        """
        if verbose is None:
            verbose = self.verbose
        with requests.Session() as s:
            payload = {
                'tday': f'{args.day:02d}',
                'tmonth': f'{args.month:02d}',
                'tyear': f'{args.year}',
                'tbegin': f'{args.arrival:02d}',
                'tend': f'{args.departure:02d}',
                'tufficio': f'{args.office}',
                'tguest': f'{args.guests}',
            }
            r = s.post('https://novnc.math.unipd.it/presenze/time.php', auth=HTTPBasicAuth(self.user, self.pwd), 
                       data=payload)
            table = utils.parse_table(r.content)
            num_rows = len(list(table.values())[0])
            table['Date'] = [f'{args.day_str} {args.year}-{args.month}-{args.day}' for _ in range(num_rows)]

            if num_rows == 0:
                if verbose:
                    logging.info(f'There are no reservations on {args.day_str[:3]} {args.year}-{args.month}-{args.day} in '
                                 f'the office {args.office}.')
            else:
                if verbose:
                    logging.info(f'Reservations on {args.day_str[:3]} {args.year}-{args.month}-{args.day} in the '
                                 f'office {args.office}:\n')
                    logging.info(utils.pretty_print(table, drop_keys=['Delete', 'ttimeid', 'Person']))
        return table

    def remove_single(self, args, verbose=None):
        """
        Remove a registration given a timeslot.
        """
        if verbose is None:
            verbose = self.verbose
        table = self.check_single(args, verbose=False)
        num_rows = len(list(table.values())[0])
        if num_rows == 0:
            logging.info(f'There are no reservations on {args.day_str[:3]} {args.year}-{args.month}-{args.day} in the '
                         f'office {args.office}.')

        # Remove all reservations for the entire day
        for i in range(num_rows):
            payload = {
                'username': self.user,
                'tday': f'{args.day:02d}',
                'tmonth': f'{args.month:02d}',
                'tyear': f'{args.year}',
                'tbegin': table['Arrival'][i],
                'tend': table['Departure'][i],
                'tufficio': table['Office'][i],
                'tguest': '',
                'ttimeid': table['ttimeid'][i],
            }
            with requests.Session() as s:
                r = s.post('https://novnc.math.unipd.it/presenze/time.php', auth=HTTPBasicAuth(self.user, self.pwd),
                           data=payload)
                r = s.post('https://novnc.math.unipd.it/presenze/delete.php', auth=HTTPBasicAuth(self.user, self.pwd),
                           data=payload)
                if 'Delete successful' in r.text:
                    logging.info(f'Reservation {args.day_str[:3]} {args.year}-{args.month}-{args.day} from '
                                 f'{table["Arrival"][i]} to {table["Departure"][i]} in the office {args.office} removed!')
                else:
                    logging.info('Reservation NOT removed!')

    def run(self, args, verbose=None):
        if args.mode == 'book':
            func = self.book_single
        elif args.mode == 'check':
            func = self.check_single
        elif args.mode == 'remove':
            func = self.remove_single
        else:
            raise Exception(f'Error. Mode "{args.mode}" is not supported.')

        days = []
        day = datetime.date.today()
        if args.this_week:
            while True:
                if day.strftime('%a') in ['Sat', 'Sun']:
                    break
                days += [day]
                day += datetime.timedelta(1)
        if args.next_week:
            weekend_passed = False
            while True:
                if day.strftime('%a') == 'Sun':
                    weekend_passed = True
                elif day.strftime('%a') == 'Sat':
                    if weekend_passed:
                        break
                else:
                    if weekend_passed:
                        days += [day]
                day += datetime.timedelta(1)
        if args.this_month:
            month = day.month + 12 * day.year
            month_passed = False
            while True:
                if (day.month + 12 * day.year - 1) == month:
                    month_passed = True
                if month_passed:
                    break
                if day.strftime('%a') not in ['Sat', 'Sun']:
                    days += [day]
                day += datetime.timedelta(1)
        if args.next_month:
            month = day.month + 12 * day.year
            month_passed = False
            while True:
                if (day.month + 12 * day.year - 1) == month:
                    month_passed = True
                if (day.month + 12 * day.year - 2) == month:
                    break
                if (day.strftime('%a') not in ['Sat', 'Sun']) and month_passed:
                    days += [day]
                day += datetime.timedelta(1)
        if args.today:
            days += [day]
        elif args.tomorrow:
            day += datetime.timedelta(1)
            days += [day]

        # loop over days
        out = []
        for day in days:
            args.day = day.day
            args.month = day.month
            args.year = day.year
            args.day_str = datetime.datetime(args.year, args.month, args.day).strftime('%a')
            out += [func(args, verbose=verbose if args.mode != 'check' else False)]
        if args.mode == 'check':
            out = utils.merge_dict(out)
            logging.info(f'Reservations on {day.month}-{day.year} in the office {args.office}:\n')
            logging.info(utils.pretty_print(out, drop_keys=['Delete', 'ttimeid', 'Person']))
        return out


if __name__ == '__main__':
    import sys
    import getpass
    import utils

    # Retrieve input args
    args = utils.get_args(sys.argv[1:])

    # Retrieve math credentials
    user = input('[Username] ') if len(args.user) == 0 else args.user
    pwd = getpass.getpass('[Password] ') if len(args.pwd) == 0 else args.pwd

    # Book
    bm = BookManager(user, pwd)
    bm.run(args)
