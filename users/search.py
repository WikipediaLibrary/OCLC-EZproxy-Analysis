from pathlib import Path
from tldextract import extract

from config import Config as config
from helpers import date_range_list, read_files


class Search:
    date_list = date_range_list(config.start_date, config.end_date)
    user_sessions = {}

    def __init__(self, search_list):
        self.search_list = search_list
        read_files(self.date_list, "ezp{}.log", self.search_in_line)
        read_files(self.date_list, "{}.txt", self.session_in_line)
        for session_id in self.user_sessions.keys():
            print(self.user_sessions[session_id])

    def search_in_line(self, line):
        for search in self.search_list:
            split_line = " ".join(line.split()).split("|")[0].strip().split(" ")
            request = split_line[6]
            if search in request:
                session_id = split_line[2]
                if session_id not in self.user_sessions:
                    self.user_sessions[session_id] = {
                        "ip": [],
                        "username": [],
                        "match": [],
                    }
                ip = split_line[0]
                if ip not in self.user_sessions[session_id]["ip"]:
                    self.user_sessions[session_id]["ip"].append(ip)
                if line not in self.user_sessions[session_id]["match"]:
                    self.user_sessions[session_id]["match"].append(line)

    def session_in_line(self, line):
        if "Login.Success" in line:
            # find the login line for matching sessions
            for session_id in self.user_sessions.keys():
                if session_id in line:
                    split_line = " ".join(line.split()).split("|")[0].strip().split(" ")
                    # capture username
                    username = " ".join(split_line[4:-1])
                    if username not in self.user_sessions[session_id]["username"]:
                        self.user_sessions[session_id]["username"].append(username)
