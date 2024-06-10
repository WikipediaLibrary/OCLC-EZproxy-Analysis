import datetime


def date_range_list(start_date, end_date):
    # Return list of datetime.date objects between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date.strftime('%Y%m%d'))
        curr_date += datetime.timedelta(days=1)
    return date_list


start_date = datetime.date(year=2022, month=11, day=1)
stop_date = datetime.date(year=2023, month=1, day=31)
date_list = date_range_list(start_date, stop_date)

file_path = 'q4'

user_sessions = {}

for date in date_list:
    user_file = file_path + '/{}.txt'.format(date)

    with open(user_file, 'r', encoding='utf-8') as user_file_open:
        file_lines = user_file_open.readlines()
        for line in file_lines:
            if "Login.Success" in line:
                split_line = " ".join(line.split()).split("|")[0].strip().split(" ")

                username = " ".join(split_line[4:-1])
                session_id = split_line[-1]

                user_sessions[session_id] = username

user_tracker = []

for date in date_list:
    user_file = file_path + '/spu{}.log'.format(date)

    with open(user_file, 'r', encoding='utf-8') as user_file_open:
        file_lines = user_file_open.readlines()
        for line in file_lines:
            if "wiley.com" in line:
                session_id = " ".join(line.split()).split(" ")[2]
                username = user_sessions[session_id]

                if username not in user_tracker:
                    user_tracker.append(username)

print(len(user_tracker))
