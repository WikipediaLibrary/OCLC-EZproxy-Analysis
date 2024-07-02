import gzip
import logging
from pathlib import Path, PurePath
import requests
import re
from sys import stderr
import urllib3

from config import Config as config
from .html_parser import LogListParser

# Setup
urllib3.disable_warnings()
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(stderr))
logger.setLevel(config.log_level)
session = requests.Session()
login_url = "https://login.{}/login".format(config.hostname)
log_list_url = "https://{}/loggedin/admlog/loglisting.htm".format(config.hostname)

# Get cookie
session.get(login_url, verify=False)
# Set form data, including our desired destination
data = {
    "user": config.user,
    "pass": config.password,
    "url": log_list_url,
}
# Login - set credentials in .env
log_list_response = session.post(login_url, data=data, verify=False, stream=True)
# Bail on error
if log_list_response.status_code != 200:
    logger.error("Login failed: HTTP {}".format(log_list_response.status_code))
    exit

# Scrape the log listing
start_date = int(config.start_date.strftime("%Y%m%d"))
end_date = int(config.end_date.strftime("%Y%m%d"))
for line in log_list_response.iter_lines():
    parser = LogListParser()
    fragment = line.decode("utf-8")
    log_types = ["spu", "auditfile"]
    # We're interested in specific log files
    if not any(log_type in fragment for log_type in log_types):
        continue
    # capture the href value in the html fragment
    parser.feed(fragment)
    # check the date embedded in the filename
    match = re.search(r"\d{8}", parser.link)
    date = int(match.group())
    if date < start_date or date > end_date:
        logger.info("{} not in date range".format(date))
        continue
    # Handle the download
    log_url = "https://wikipedialibrary.idm.oclc.org/loggedin/admlog/{}".format(
        parser.link
    )
    log_purepath = PurePath(parser.link)
    log_filepath = "./data/{}".format(log_purepath.name)
    if log_purepath.suffix == ".gz":
        log_filepath = "./data/{}".format(log_purepath.stem)
    local_log_file = Path(log_filepath)
    if local_log_file.is_file():
        logger.info("{} exists; skipping download".format(log_filepath))
        continue
    print("fetching {}".format(log_url))
    log_file_response = session.get(log_url)
    if log_file_response.status_code != 200:
        logger.error("Download error: HTTP {}".format(log_file_response.status_code))
        continue
    if log_purepath.suffix == ".gz":
        logger.info("decompressing {}".format(log_url))
        content = gzip.decompress(log_file_response.content)
    else:
        content = log_file_response.content
    logger.info("saving {}".format(log_filepath))
    open(log_filepath, "wb").write(content)
