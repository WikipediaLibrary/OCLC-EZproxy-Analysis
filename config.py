from datetime import date
from dotenv import load_dotenv, dotenv_values
from os import getenv

load_dotenv()


class Config:
    hostname = str(getenv("hostname", "ezproxy.dev.localdomain:2048"))
    user = str(getenv("user", "someuser"))
    password = str(getenv("password", "somepass"))
    start_date = date.fromisoformat(str(getenv("start_date", 20240101)))
    end_date = date.fromisoformat(str(getenv("end_date", 20240630)))
    partner_search = str(getenv("partner_search", "search.worldcat.org"))
