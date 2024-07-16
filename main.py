from fetch import fetch

log_types = ["spu", "auditfile"]
fetch_count = fetch.Fetch(log_types)

from count import users
