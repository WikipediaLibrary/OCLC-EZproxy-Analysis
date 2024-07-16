from datetime import timedelta
from pathlib import Path
from tldextract import extract

from config import Config as config
from helpers import date_range_list

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
all_users = []

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
                if username not in all_users:
                    all_users.append(username)
                if domain not in tracker:
                    tracker[domain] = {}
                if vhost not in tracker[domain]:
                    tracker[domain][vhost] = []
                if username not in tracker[domain][vhost]:
                    tracker[domain][vhost].append(username)

ordered_tracker = dict(sorted(tracker.items()))
banner = "unique ezproxy users {start_date}-{end_date} (inclusive): {total_count}"
print(
    banner.format(
        start_date=config.start_date,
        end_date=config.end_date,
        total_count=len(all_users),
    )
)
for domain in ordered_tracker:
    domain_users = []
    domain_template = "{domain}: {count}"
    vhost_template = "{vhost}: {count}"
    multi_vhosts = len(ordered_tracker[domain]) > 1
    vhost_data = []
    for vhost in ordered_tracker[domain]:
        vhost_users = ordered_tracker[domain][vhost]
        count = len(vhost_users)
        # Track unique users across subdomains
        if multi_vhosts:
            vhost_template = " - {vhost}: {count}"
            for username in vhost_users:
                if username not in domain_users:
                    domain_users.append(ordered_tracker[domain][vhost])
        vhost_data.append(vhost_template.format(vhost=vhost, count=count))
    if domain_users:
        count = len(domain_users)
        print(domain_template.format(domain=domain, count=count))
    for data in vhost_data:
        print(data)
