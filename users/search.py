from pathlib import Path
from tldextract import extract

from config import Config as config
from helpers import LOG_TYPES, date_range_list, read_files


class Search:
    date_list = date_range_list(config.start_date, config.end_date)
    user_sessions = {}

    def __init__(self, search_list):
        self.search_list = search_list
        read_files(self.date_list, LOG_TYPES["ezp"], self.search_in_line)
        read_files(self.date_list, LOG_TYPES["auditfile"], self.session_in_line)
        report_data = ["results:\n"]
        session_template = "session_id: {session_id}"
        username_template = "\tuser: {username}"
        match_template = "\t\t{match}"
        for session_id in self.user_sessions.keys():
            report_data.append(session_template.format(session_id=session_id))
            for username in self.user_sessions[session_id]["username"]:
                report_data.append(username_template.format(username=username))
            match_data = "\tlog_entries:\n"
            for match in self.user_sessions[session_id]["match"]:
                match_data += match_template.format(match=match)
            report_data.append(match_data)
        for line in report_data:
            print(line)

    def search_in_line(self, line):
        for search in self.search_list:
            # it's fastest to check the whole line first
            if search not in line:
                continue
            # then check the request in particular
            split_line = " ".join(line.split()).split("|")[0].strip().split(" ")
            request = split_line[6]
            if search not in request:
                continue
            session_id = split_line[2]
            if session_id not in self.user_sessions:
                self.user_sessions[session_id] = {
                    "username": [],
                    "match": [],
                }
            if line not in self.user_sessions[session_id]["match"]:
                self.user_sessions[session_id]["match"].append(line)

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
