from Models.db.MongoModels import DB
import json
import uuid
#
from misc.lib.snpy import parse


class REPORT_ID:
    def __init__(self):
        self.db_init = DB(collection='reports')
        pass

    def generate(self):
        id = str(uuid.uuid4())
        return id

    def insert(self, id):
        self.db_init.insert({'report_id': id})


class REPORT_FILE:
    def __init__(self, file, source):
        self.file = file
        self.source = source

    def load(self):
        try:
            parsed_filed = parse(self.file, source=self.source)
            return {p.name: p.genotype for p in parsed_filed}

        except Exception as e:
            return False


class REPORT_MATCH:
    def __init__(self, genome_file):
        self.genome_file = genome_file
        pass

    def clean_up_gene(self, old_gene):
        return ''.join(filter(str.isalpha, old_gene))

    def rsid(self, user_rsid):
        try:
            return self.genome_file[user_rsid]
        except:
            return False

    def gene(self, user_rsid, user_gene):
        if str(self.genome_file[user_rsid]) == self.clean_up_gene(user_gene):
            return self.clean_up_gene(user_gene)
        else:
            return False


class REPORT_BUILD:
    def __init__(self, genome_file, mag):
        self.genome_file = genome_file
        self.mag = mag
        pass

    def uniquify(self, my_list):
        seen = set()
        new_list = []
        for item in my_list:
            gene = item['gene']
            if gene not in seen:
                seen.add(gene)
                new_list.append(item)

        return new_list

    def return_snps_from_genes(self, genes_list):
        db_connection = DB('snps')

        magnitude_query = {"genes": {'$elemMatch': {
            'magnitude': {'$gt': float(self.mag)}}}}
        gene_query = {"gene": {"$in": genes_list}}

        master_query = {"$and": [magnitude_query, gene_query]}

        results = db_connection.search_db(master_query)

        return db_connection.return_as_json(results)

    def generate_report(self, db_base_query, keyword=None):
        match = REPORT_MATCH(self.genome_file)
        base_list = []
        for db_snp in db_base_query['response']:
            db_rsid = db_snp['rsid']
            if match.rsid(db_rsid) is not False:

                for db_gene in db_snp['genes']:
                    db_geno = db_gene['gene']
                    db_geno_user_match = match.gene(db_rsid, db_geno)
                    if db_geno_user_match and db_gene['magnitude'] >= self.mag:
                        j = {}
                        j['rsid'] = db_rsid
                        j['geno'] = db_geno
                        j['gene'] = db_snp['gene']
                        j['mag'] = db_gene['magnitude']
                        j['summary'] = db_gene['summary']
                        j['repute'] = db_gene['repute']

                        # if keyword exists
                        if keyword:
                            j['tag'] = keyword
                        else:
                            j['tag'] = 'None'

                        base_list.append(j)

        return base_list
