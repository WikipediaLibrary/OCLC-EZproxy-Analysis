from datetime import timedelta
from pathlib import Path
from tldextract import extract

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

tracker = {}

for date in date_list:
    user_file = Path(file_path + "/spu{}.log".format(date))
    if not user_file.is_file():
        print("{} not found".format(user_file))
        continue
    with open(user_file, "r", encoding="utf-8") as user_file_open:
        file_lines = user_file_open.readlines()
        for line in file_lines:
            line_split = line.split()
            session_id = line_split[2]
            access = line_split[3]
            vhost = line_split[4]
            domain = extract(vhost).registered_domain
            if access == "proxy" and session_id in user_sessions:
                username = user_sessions[session_id]
                if domain not in tracker:
                    tracker[domain] = {}
                if vhost not in tracker[domain]:
                    tracker[domain][vhost] = []
                if username not in tracker[domain][vhost]:
                    tracker[domain][vhost].append(username)

ordered_tracker = dict(sorted(tracker.items()))
print("unique ezproxy users by domain and host:")
for domain in ordered_tracker:
    print("{}:".format(domain))
    domain_users = []
    for vhost in ordered_tracker[domain]:
        vhost_users = ordered_tracker[domain][vhost]
        count = len(vhost_users)
        data = "\t{vhost}:\t{count}"
        print(data.format(vhost=vhost, count=count))
        for username in vhost_users:
            if username not in domain_users:
                domain_users.append(ordered_tracker[domain][vhost])
    count = len(domain_users)
    data = "\ttotal:\t{count}"
    print(data.format(domain=domain, count=count))
