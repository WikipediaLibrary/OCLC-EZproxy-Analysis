import datetime
import requests
from dotenv import load_dotenv, dotenv_values
import os
import requests
import urllib3

load_dotenv()
urllib3.disable_warnings()

def date_range_list(start_date, end_date):
    # Return list of datetime.date objects between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date.strftime('%Y%m%d'))
        curr_date += datetime.timedelta(days=1)
    return date_list


start_date = datetime.date(year=2023, month=12, day=1)
stop_date = datetime.date(year=2024, month=6, day=1)
date_list = date_range_list(start_date, stop_date)

s = requests.Session()

login_url = 'https://login.wikipedialibrary.idm.oclc.org/login'
log_list_url = 'https://wikipedialibrary.idm.oclc.org/loggedin/admlog/loglisting.htm'

# Get cookie
s.get(login_url, verify=False)

# Login - set credentials in .env
login_response = s.post(login_url, data={'user': os.getenv('user', ''), 'pass': os.getenv('password', '')}, verify=False)

response = s.get(log_list_url, verify=False)

session_partner_url = "https://wikipedialibrary.idm.oclc.org/loggedin/admaudit/{}.txt"
user_session_url = "https://wikipedialibrary.idm.oclc.org/loggedin/admlog/spu{}.log"  # Can also be .gz  # Needs to be manually downloaded.
for date in date_list:
    session_partner_file = s.get(session_partner_url.format(date))
    open('data/{}.txt'.format(date), 'wb').write(session_partner_file.content)
