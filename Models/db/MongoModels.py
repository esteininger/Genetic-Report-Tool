from Utilities.Database import mongoDBConnect
import json
import uuid

class DB:
	def __init__(self, collection):
		self.collection = collection
		pass

	def mongo_connect(self):
		return mongoDBConnect()[self.collection]

	def return_as_json(self, result):
		j = {}
		j['response'] = [doc for doc in result]
		j['count'] = result.count()
		return j

	def insert(self, inserted_dict):
		return self.mongo_connect().insert(inserted_dict)

	def delete_one(self, query):
		# keep it
		try:
			self.search_db_one(query)['stay']
		except KeyError:
			self.mongo_connect().delete_one(query)
			pass

	def update(self, query, updated_dict):
		return self.mongo_connect().update_one(query, {"$set": updated_dict}, upsert=False)

	def search_db(self, query):
		return self.mongo_connect().find(query, {'_id': False})

	def search_db_one(self, query):
		return self.mongo_connect().find_one(query, {'_id': False})

	def generate_id(self):
		id = str(uuid.uuid1())
		return id
