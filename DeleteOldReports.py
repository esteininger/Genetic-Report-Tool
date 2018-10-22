#!/usr/bin/python3.6

from Utilities.Database import mongoDBConnect
from time import time

db_init = mongoDBConnect()['reports']

two_days_of_seconds = 172800
two_days_ago = time() - two_days_of_seconds

db_init.remove({"timestamp": {"$lt": two_days_ago}})
