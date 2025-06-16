from datetime import timedelta
import pymysql.cursors
from pathlib import Path

LOG_TYPES = {"auditfile": "{}.txt", "ezp": "ezp{}.log", "spu": "spu{}.log"}


def date_range_list(start_date, end_date):
    # Return list of date objects between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date.strftime("%Y%m%d"))
        curr_date += timedelta(days=1)
    return date_list


def read_files(date_list, filename_template, callback):
    file_path = "data/"
    for date in date_list:
        user_file = Path(file_path + filename_template.format(date))
        if not user_file.is_file():
            print("{} not found".format(user_file))
            continue

        with open(user_file, "r", encoding="utf-8") as user_file_open:
            file_lines = user_file_open.readlines()
            for line in file_lines:
                callback(line)


def db_cursor(db_config):
    connection = pymysql.connect(
        user=db_config["user"],
        password=db_config["pw"],
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["db"],
    )
    return connection.cursor()
