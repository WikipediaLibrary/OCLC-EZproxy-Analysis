#!/usr/bin/env python
from argparse import ArgumentParser
from fetch import fetch

from users import list

parser = ArgumentParser(description="Search for users by request path")
parser.add_argument("search", metavar="S", type=str, nargs="+")

args = parser.parse_args()

log_types = ["spu", "auditfile"]
fetch_count = fetch.Fetch(log_types)
user_search = list.Search(args.search)
