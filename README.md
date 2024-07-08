# OCLC EZproxy Log Analysis

Download, parse, and analyse EZproxy logs


## Usage

1. copy example.env to .env
2. update variables to match your server and desired reporting dates
3. create and configure python virtual environment
    - `python3 -m venv venv`
    - `. venv/bin/activate`
    - `pip install -r requirements.txt`
4. run script
    - `python main.py`
    - you may redirect output to file if you desire, eg. `python main.py > ~/exproxy.usercount.20240101-20240630.md`
