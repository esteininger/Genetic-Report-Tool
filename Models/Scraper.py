import json
import requests
import mwparserfromhell
from pprint import pprint
import collections
from bs4 import BeautifulSoup
import time

class MakeGeneFile:
    def __init__(self):
        pass

    def write(self, list):
        with open('genes_1.txt', 'a') as f:
            for item in list:
                f.write("%s\n" % item)

    def soup(self, url=None):
        base_url = 'https://bots.snpedia.com/index.php?title=Category:Is_a_snp'

        if url is not None:
            url = base_url + '&' + url
        else:
            url = base_url

        return BeautifulSoup(requests.get(url).content, "html5lib")

    def iterate(self, url):
        try:
            soup = self.soup(url)
            divContent = soup.find_all('div', {"class":"mw-category-group"})

            snpList = []
            for ul in divContent:
                for li in ul.find_all('ul'):
                    anchor = li.find_all('a')
                    for text in anchor:
                        snpList.append(text.text)

            self.write(snpList)
            new_url = soup.findAll('a', href=True, text='next page')[0]['href'].split('&')[1]
            print (new_url)
            # time.sleep(1)
            self.iterate(new_url)

        except Exception as e:
            print (e)
            pass

class Scraper:
    def __init__(self):
        self.base_url = 'https://bots.snpedia.com/api.php'
        self.sesh = requests.session()
        pass

    def get_value(self, t, tag):
        return str(t.get(tag).value).strip()

    def query(self, search):
        #print('search', search)
        params = {
            'format':'json',
            'action':'query',
            'prop':'revisions',
            'rvprop':'content',
            'titles':search
        }
        res = self.sesh.get(self.base_url, params=params).json()

        #print(res)

        pages = res["query"]["pages"]
        text = list(pages.values())[0]["revisions"][0]["*"]

        wikicode = mwparserfromhell.parse(text)

        return wikicode

    def get_genos(self, rsid):
        result = collections.OrderedDict(gene="", rsid="", CLNDBN="", genes=[])
        wikicode = self.query(rsid)
        genos = ['geno1', 'geno2', 'geno3']
        template = wikicode.filter_templates()[0]

        result['rsid'] = rsid
        result['gene'] = str(template.get("Gene").value).strip()

        for i in range(0, len(wikicode.filter_templates())):
            try:
                t = wikicode.filter_templates()[i]
                result["CLNDBN"] = str(t.get("CLNDBN").value).strip()
            except:
                pass

        result['rsid'] = rsid

        genes = []
        i = 0
        while True:
            try:
                i = i + 1
                gene = 'geno' + str(i)
                gene_name = str(template.get(gene).value).strip()
                geno_info = self.query(rsid + gene_name)
                gen_template = geno_info.filter_templates()[0]
                gene = {}
                gene['gene'] = gene_name

                try:
                    gene["magnitude"] = get_value(gen_template, "magnitude")
                except:
                    pass

                try:
                    gene["repute"] = get_value(gen_template, "repute")
                except:
                    pass

                try:
                    gene["summary"] = get_value(gen_template, "summary")
                except:
                    pass

                genes.append(gene)
            except Exception as e:
                print (e)
                break

        result['genes'] = genes
        r = json.dumps(result)
        return r


from pymongo import MongoClient, GEO2D

def mongoDBConnect():
    client = MongoClient('mongodb://localhost:27017/')
    db_session = client['test']
    return db_session


#test
scraper = Scraper()
mgdb = mongoDBConnect()
gene_dict = json.loads(scraper.get_genos('rs1815739'))
print (gene_dict)
theVar = 'hi'

# mgdb.genes.insert_one(gene_dict)





# def iterateFile():
#     scraper = Scraper()
#     mgdb = mongoDBConnect()
#
#     with open('genes.txt') as f:
#         for line in f:
#             line = line.strip()
#             try:
#                 gene_dict = json.loads(scraper.get_genos(line))
#                 mgdb.genes.insert_one(gene_dict)
#                 print (line + ' added!')
#             except:
#                 print (line + ' skipped!')
#                 pass

# iterateFile()
