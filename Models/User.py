from Utilities.Database import mongoDBConnect

class UserDB:
	def __init__(self):
		pass

	@staticmethod
	def mongo_connect():
		return mongoDBConnect()['profiles']

	@staticmethod
	def return_as_json(result):
		j = {}
		j['response'] = [doc for doc in result]
		j['count'] = result.count()
		return j

class User:
	def __init__(self):
		pass

	def add(self, json):
		return UserDB.mongo_connect().insert_one(json)
