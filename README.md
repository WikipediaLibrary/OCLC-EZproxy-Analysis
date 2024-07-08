# OCLC EZproxy Log Analysis

Download, parse, and analyse EZproxy logs


## Usage

1. download this repository
    - `git clone https://github.com/WikipediaLibrary/OCLC-EZproxy-Analysis.git`
    - `cd OCLC-EZproxy-Analysis`
1. copy example.env to .env
1. update variables to match your server and desired reporting dates
1. create and configure python virtual environment
    - `python3 -m venv venv`
    - `. venv/bin/activate`
    - `pip install -r requirements.txt`
1. run script
    - `python main.py`
    - you may redirect output to file if you desire, eg. `python main.py > ~/exproxy.usercount.20240101-20240630.md`
