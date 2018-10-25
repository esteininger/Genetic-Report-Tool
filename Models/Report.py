from Utilities.Database import mongoDBConnect
from arv import load, unphased_match as match
import json
import uuid

class ReportDB:
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


class ReportID:
	def __init__(self):
		self.db_init = ReportDB(collection='reports')
		pass

	def generate(self):
		id = str(uuid.uuid4())
		return id

	def insert(self, id):
		self.db_init.insert({'report_id': id})

	# def retrieve(self, report_id):
	# 	return self.db_init.search_db_one(query = {'report_id':id})
	#
	# def update(self, report_id):


class ReportFile:
	def __init__(self, file, source_site=None):
		self.source_site = source_site
		self.file = file

	def load_file(self):
		try:
			return load(self.file)
		except:
			return False


class ReportBuild:
	def __init__(self, genome_file):
		self.genome_file = genome_file
		pass

	def clean_up_gene(self, old_gene):
		return ''.join(filter(str.isalpha, old_gene))

	def uniquify(self, my_list):
		seen = set()
		new_list = []
		for item in my_list:
		    gene = item['gene']
		    if gene not in seen:
		        seen.add(gene)
		        new_list.append(item)

		return new_list

	def match_rsid(self, user_rsid):
		try:
			return self.genome_file[user_rsid]
		except Exception as e:
			return False

	def match_gene(self, user_rsid, user_gene):
		if str(self.genome_file[user_rsid]) == self.clean_up_gene(user_gene):
			return self.clean_up_gene(user_gene)
		else:
			return False

	def base_query(self, collection, query, mag):
		db_connection = ReportDB(collection)

		magnitude_query = {"genes": {'$elemMatch': {'magnitude': {'$gt': float(mag)}}}}
		master_query = {"$and": [magnitude_query, query]}

		results = db_connection.search_db(master_query)

		return db_connection.return_as_json(results)

	def generate_report(self, mag, db_base_query):
		# run inside a thread and output progress bar as event stream
		base_list = []
		for db_snp in db_base_query['response']:
			db_rsid = db_snp['rsid']
			db_rsid_user_match = self.match_rsid(db_rsid)
			if db_rsid_user_match:
				for db_gene in db_snp['genes']:
					db_geno = db_gene['gene']
					db_geno_user_match = self.match_gene(db_rsid, db_geno)
					if db_geno_user_match and db_gene['magnitude'] >= mag:
						j = {}
						j['rsid'] = db_rsid
						j['geno'] = db_geno
						j['gene'] = db_snp['gene']
						j['mag'] = db_gene['magnitude']
						j['summary'] = db_gene['summary']
						j['repute'] = db_gene['repute']
						j['tag'] = db_snp['tags']
						base_list.append(j)

		return base_list
