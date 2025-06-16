from csv import QUOTE_ALL, writer
from datetime import datetime
from pathlib import Path
from tldextract import extract

from config import Config as config
from helpers import LOG_TYPES, date_range_list, read_files

from .twlight import TWLightUser


class Search:
    date_list = date_range_list(config.start_date, config.end_date)
    user_sessions = {}
    twlight = TWLightUser()

    def __init__(self, search_list):
        for search in search_list:
            self.search = search
            read_files(self.date_list, LOG_TYPES["spu"], self.search_in_line)
            read_files(self.date_list, LOG_TYPES["auditfile"], self.session_in_line)
            report_file = "output/userlist_{search}_{start}-{end}.csv".format(
                search=search, start=config.start_date, end=config.end_date
            )
            with open(report_file, "w") as csv:
                write = writer(csv, quoting=QUOTE_ALL)
                user_set = set()
                for session_id in self.user_sessions.keys():
                    for username in self.user_sessions[session_id]["username"]:
                        user_set.add(username)
                for username in user_set:
                    email = self.twlight.get_email(username)
                    write.writerow([username, email])

    def search_in_line(self, line):
        # it's fastest to check the whole line first
        if self.search not in line:
            return
        # then check the vhost in particular
        split_line = " ".join(line.split()).split("|")[0].strip().split(" ")
        vhost = split_line[4]
        if self.search not in vhost:
            return
        session_id = split_line[2]
        if session_id not in self.user_sessions:
            self.user_sessions[session_id] = {
                "username": [],
            }

    def session_in_line(self, line):
        if "Login.Success" not in line:
            return
        # find the login line for matching sessions
        for session_id in self.user_sessions.keys():
            if session_id not in line:
                continue
            split_line = " ".join(line.split()).split("|")[0].strip().split(" ")
            # capture username
            username = " ".join(split_line[4:-1])
            if username not in self.user_sessions[session_id]["username"]:
                self.user_sessions[session_id]["username"].append(username)
