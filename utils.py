import argparse
import datetime
from lxml import etree
import pandas as pd


def get_args(stdin):
    """
    Parse input arguments.
    """
    now = datetime.datetime.now()
    parser = argparse.ArgumentParser(stdin)
    parser.add_argument('--mode', type=str, default='book', help='Year of the booking.', 
                        choices=['book', 'check', 'remove'])
    parser.add_argument('--year', type=int, default=now.year, help='Year of the booking.', choices=[2020, 2021, 2022])
    parser.add_argument('--month', type=int, default=now.month, 
                        help='Month number of the booking.', choices=list(range(1, 13)))
    parser.add_argument('--day', type=int, default=now.day, help='Day of the booking.')
    parser.add_argument('--arrival', type=int, default=9,
                                            help='Time of arrival (h) of the booking.', choices=list(range(7, 19)))
    parser.add_argument('--departure', type=int, default=18,
                                            help='Time of departure (h) of the booking.', choices=list(range(8, 20)))
    parser.add_argument('--office', type=int, default=732, help='Office number.')
    parser.add_argument('--guests', type=str, default='', help='Guests names (optional).')

    parser.add_argument('--today', action='store_true', default=True, help='Use today as the time reference.')
    parser.add_argument('--tomorrow', action='store_true', help='Use tomorrow as the time reference.')
    parser.add_argument('--this_week', action='store_true', help='Use this week as the time reference.')
    parser.add_argument('--next_week', action='store_true', help='Use next week as the time reference.')
    parser.add_argument('--this_month', action='store_true', help='Use this month as the time reference.')
    parser.add_argument('--next_month', action='store_true', help='Use next month as the time reference.')
    parser.add_argument('--user', type=str, default='', help='Math username.')
    parser.add_argument('--pwd', type=str, default='', help='Math password.')
    args = parser.parse_args()

    # Process input args
    args.day_str = datetime.datetime(args.year, args.month, args.day).strftime('%a')
    if args.tomorrow:
        args.today = False
    return args

def parse_table(content):
    """
    Scrape table from HTML.
    """
    table = etree.HTML(content).find('body/table')
    cols = iter(table)
    table_dict = {col.text: [] for col in next(cols)}
    headers = list(table_dict.keys())
    table_dict['ttimeid'] = []
    for i, col in enumerate(cols):
        ttimeid = etree.HTML(content).xpath('//*[@id="chooseday"]/input[8]')[i]
        ttimeid = etree.tostring(ttimeid).decode('utf-8').split('value=')[1].replace('/>', '').replace('"', '').strip()
        table_dict['ttimeid'] += [ttimeid]
        
        for h, c in zip(headers, col):
            table_dict[h] += [c.text]
    return table_dict

def pretty_print(dict_, drop_keys=[]):
    df = pd.DataFrame(dict_)
    df = df.drop(labels=drop_keys, axis=1)
    df = df.rename(columns={c: c[:3] for c in df.columns})
    return df.to_markdown(index=False, tablefmt='simple')

def merge_dict(dict_list):
    if len(dict_list) == 0:
        return {}
    dict_ = {h: [] for h in dict_list[0].keys()}
    for d in dict_list:
        for k, v in d.items():
            dict_[k] += v
    return dict_
