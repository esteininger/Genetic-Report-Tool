from .db.MongoModels import DB
import json


class Office:
    def __init__(self, office_id=None):
        self.connect = DB(collection="office")
        self.office_id = office_id

    def insert(self, dict):
        return self.connect.insert(dict)

    def unique_id(self):
        return self.connect.generate_id()

    def find_one(self):
        return self.connect.search_db_one({"office_id": self.office_id})

    def get_genes_and_keywords(self, query=None):
        filters = []
        if query is not None:
            query = self.find_one()

        for item in query['keyword_genes']:
            g = {}
            g['keyword'] = item['keyword']
            g['gene'] = item['genes']
            filters.append(g)

        return filters


# class ReportDB:
# 	def __init__(self, collection):
# 		self.collection = collection
# 		pass
