from datetime import timedelta
from pathlib import Path

from config import Config as config


def date_range_list(start_date, end_date):
    # Return list of date objects between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date.strftime("%Y%m%d"))
        curr_date += timedelta(days=1)
    return date_list


date_list = date_range_list(config.start_date, config.end_date)

file_path = "data"

user_sessions = {}

for date in date_list:
    user_file = file_path + "/{}.txt".format(date)

    with open(user_file, "r", encoding="utf-8") as user_file_open:
        file_lines = user_file_open.readlines()
        for line in file_lines:
            if "Login.Success" in line:
                split_line = " ".join(line.split()).split("|")[0].strip().split(" ")

                username = " ".join(split_line[4:-1])
                session_id = split_line[-1]

                user_sessions[session_id] = username

user_tracker = []

for date in date_list:
    user_file = Path(file_path + "/spu{}.log".format(date))
    if not user_file.is_file():
        print("{} not found".format(user_file))
        continue
    with open(user_file, "r", encoding="utf-8") as user_file_open:
        file_lines = user_file_open.readlines()
        for line in file_lines:
            if config.partner_search in line:
                session_id = " ".join(line.split()).split(" ")[2]
                username = user_sessions[session_id]

                if username not in user_tracker:
                    user_tracker.append(username)

print(len(user_tracker))
