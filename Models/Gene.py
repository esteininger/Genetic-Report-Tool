from .db.MongoModels import DB
import json

class Gene:
    def __init__(self):
        self.connect = DB(collection="genes")

    def search(self, keyword, limit):
        #https://stackoverflow.com/questions/48371016/pymongo-how-to-use-full-text-search
        query = {"$text": {"$search": keyword}}
        resp = self.connect.search_db(query).limit(limit)
        return self.connect.return_as_json(resp)

# class ReportDB:
# 	def __init__(self, collection):
# 		self.collection = collection
# 		pass
