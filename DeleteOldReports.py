from Utilities.Database import mongoDBConnect
from time import time

db_init = mongoDBConnect()['reports']

two_days_of_seconds = 172800
compare_against = time() + two_days_of_seconds

db_init.remove({"timestamp": {"$gt": compare_against}})
