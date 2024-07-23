#!/usr/bin/env python
from fetch import fetch

log_types = ["spu", "auditfile"]
fetch_count = fetch.Fetch(log_types)

from users import count
