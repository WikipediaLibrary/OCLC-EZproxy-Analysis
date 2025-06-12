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
    log_level = str(getenv("log_level", "error")).upper()
    twlight_db = {
        "db": str(getenv("twlight_db")),
        "user": str(getenv("twlight_db_user")),
        "pw": str(getenv("twlight_db_pw")),
        "host": str(getenv("twlight_db_host")),
        "port": int(getenv("twlight_db_port")),
    }
