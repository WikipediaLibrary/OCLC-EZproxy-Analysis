import requests
from dotenv import load_dotenv, dotenv_values
import os
import requests
import urllib3
import re
from pathlib import Path, PurePath


from parser import LogListParser

load_dotenv()
urllib3.disable_warnings()

start_date = 20231201
end_date = 20240601
session = requests.Session()
hostname = os.getenv('hostname', '')
login_url = 'https://login.{}/login'.format(hostname)
log_list_url = 'https://{}/loggedin/admlog/loglisting.htm'.format(hostname)

# Get cookie
session.get(login_url, verify=False)
# Set form data, including our desired destination
data = {
    'user': os.getenv('user', ''),
    'pass': os.getenv('password', ''),
    'url': log_list_url,
}
# Login - set credentials in .env
response = session.post(
    login_url,
    data=data,
    verify=False,
    stream=True
)
# Bail on error
if response.status_code != 200:
    exit
# Scrape the log listing
for line in response.iter_lines():
    parser = LogListParser()
    fragment = line.decode('utf-8')
    log_types = ['spu', 'auditfile']
    # We're interested in specific log files
    if not any(log_type in fragment for log_type in log_types):
        continue
    # capture the href value in the html fragment
    parser.feed(fragment)
    # check the date embedded in the filename
    match = re.search(r'\d{8}', parser.link)
    date = int(match.group())
    if date < start_date or date > end_date:
        print('{} not in date range'.format(date))
        continue
    # Handle the download
    log_url = 'https://wikipedialibrary.idm.oclc.org/loggedin/admlog/{}'.format(parser.link)
    log_filepath = 'data/{}'.format(PurePath(parser.link).name)
    local_log_file = Path(log_filepath)
    if local_log_file.is_file():
        print('{} exists; skipping download'.format(log_filepath))
        continue
    print('fetching {}'.format(log_url))
    remote_log_file = session.get(log_url)
    open(log_filepath, 'wb').write(remote_log_file.content)
