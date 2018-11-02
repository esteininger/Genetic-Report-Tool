import json
import requests
import collections
import lxml
from lxml import etree
from lxml import html
import re

import logging
logging.basicConfig()

base_url = 'https://bots.snpedia.com/api.php'
sesh = requests.session()

result = collections.OrderedDict(gene="", rsid="", CLNDBN="", genes=[])

def get_genos(search):
    path = "https://www.snpedia.com/index.php/" + search
    r = sesh.get(path)
    root = html.fromstring(r.text)
    genes = []

    result['rsid'] = search

    #GENE NAME
    for tr in root.xpath('//table//tr'):
        try:
            td1 = tr.xpath('./td[1]//text()')[0].strip()
            td2 = tr.xpath('./td[2]//text()')[0].strip()

            if "Gene" in td1:
                result['gene'] = td2

        except:
            pass

    #CLNDBN
    for tr in root.xpath('//table//tr'):
        try:
            th1 = tr.xpath('./th[1]//text()')[0].strip()
            td1 = tr.xpath('./td[1]//text()')[0].strip()


            if "CLNDBN" in th1:
                result["CLNDBN"] = td1
        except:
            pass

    #get all genes
    tables = root.xpath('//table[contains(@class, "sortable ")]')

    gene = {}

    if len(tables) > 0:
        for table in tables:
            tbody = table.xpath('./tbody')[0]
            pattern = re.compile("\(.*;.*\)")
            for row in tbody.xpath('./tr'):
                gene = {}
                try:
                    gene_name = row.xpath('./td[1]/a/text()')[0].strip()

                    if row.xpath('./td[2][contains(@style, "80ff80")]'):
                        repute = "Good"
                    elif row.xpath('./td[2][contains(@style, "ff8080")]'):
                        repute = "Bad"
                    else:
                        repute = ""

                    magnitude = row.xpath('./td[2]/text()')[0].strip()
                    summary = row.xpath('./td[3]/text()')[0].strip()

                    if not pattern.match(gene_name):
                        print("not matchih", gene_name)
                        continue

                    gene['gene'] = gene_name
                    gene["magnitude"] = magnitude
                    gene["repute"] = repute
                    gene["summary"] = summary
                    gene["type"] = table.xpath('.//th[1]/text()')[0].strip().lower().replace("o", "e")
                    genes.append(gene)
                except Exception as e:
                    pass

    result['genes'] = genes

    r = json.dumps(result, indent=4)
    return r

from pymongo import MongoClient, GEO2D

def mongoDBConnect():
    client = MongoClient('mongodb://localhost:27017/')
    db_session = client['test']
    return db_session

def iterateFile():
    mgdb = mongoDBConnect()

    with open('genes.txt') as f:
        for line in f:
            line = line.strip()
            try:
                gene_dict = json.loads(get_genos(line))
                mgdb.genes.insert_one(gene_dict)
                print (line + ' added!')
            except:
                print (line + ' skipped!')
                pass

iterateFile()
