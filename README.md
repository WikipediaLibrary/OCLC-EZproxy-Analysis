# OCLC EZproxy Log Analysis

Download, parse, and analyse EZproxy logs

### User Count:

Provides a count of unique users for each proxied domain and hostname found in the selected ezproxy logs

### User Search:

Finds usernames correlated to one or more requests; typically used when a proxied resource provider detects abuse and is requesting a user block

## Setup

1. download this repository
    - `git clone https://github.com/WikipediaLibrary/OCLC-EZproxy-Analysis.git`
    - `cd OCLC-EZproxy-Analysis`
1. copy example.env to .env
1. update variables to match your server and desired reporting dates
1. create and configure python virtual environment
    - `python3 -m venv venv`
    - `. venv/bin/activate`
    - `pip install -r requirements.txt`

## Usage
User count:
- `./user_count.py`

User search:
- `./user_search.py "https://database-partner.example.com/request-path1" "/request-path2"` ...
- arguments may be full request URLs or paths

Note:
- you may redirect output from either script to a file if you desire, eg. `./user_count.py > ~/exproxy.usercount.20240101-20240630.md`
