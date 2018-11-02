from gevent.pool import Pool
import gevent.monkey
gevent.monkey.patch_all(thread=False)
import requests
import os
import webbrowser
import requests
import json
from lxml import html
from gevent import local
import random
import time
import datetime
from itertools import product
import re
import traceback
from lxml import etree
import queue
import lxml
from lxml.etree import tostring
import threading

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


class GenesParser:
    genes = []
    base = "https://snpedia.com"
    headers = {}

    def __init__(self):
        pass

    def parse(self):
        self.result_queue = queue.Queue()

        self.get_urls("/index.php/Category:Is_a_gene")
        print(len(self.genes))

        self.spawn_pools(self.genes, self.result_queue, self.fetch)
        records = []
        while True:
            try:
                record = self.result_queue.get_nowait()
                records.append(record)
            except Exception:
                break

        return records


    def get_urls(self, url):
        response = requests.get(self.base + url, timeout=10)
        r = html.fromstring(response.text)

        #get genes
        genes_ = r.xpath('//div[@id="mw-pages"]//li//a/@href')
        self.genes.extend(genes_)
        #return

        try:
            next_page = r.xpath('//a[text()="next page"]/@href')[0]
        except:
            return

        if len(next_page) > 0:
            print("next page ", next_page)
            self.get_urls(next_page)


    def spawn_pools(self, urls_chunk, queue, func):
        print("Process spawned")
        pool = Pool(50)
        glets = []

        for url in urls_chunk:
            g = pool.spawn(func, (url, queue, pool,))
            glets.append(g)

        pool.join()
        return [g.value for g in glets]

    response = None
    def fetch(self, data):
        url, queue, _ = data
        gene = {}
        while True:
            try:
                user_agent = random.choice(user_agent_list)

                self.headers['User-Agent'] = user_agent

                self.response = requests.get(self.base + url, headers=self.headers, timeout=10)
                r = html.fromstring(self.response.text, parser=etree.HTMLParser(remove_comments=True))

                gene["gene"] = r.xpath('//h1[@id="firstHeading"]/text()')[0]

                trs = r.xpath('//table//tr')

                if gene["gene"] == "":
                    raise ValueError("No data")

                i = 0
                for tr in trs:
                    try:
                        tds = tr.xpath('.//td')
                        if tds[0].xpath("./b/text()")[0] == "Full name":
                            gene["Full name"] = tds[1].text
                    except:
                        pass

                tree = r.xpath('//div[contains(@id, "mw-content-text")]//div[contains(@class, "mw-parser-output")]')[0]

                for bad in tree.xpath("//*[contains(@style, 'right')]"):
                    bad.getparent().remove(bad)

                for bad in tree.xpath(".//*[contains(text(), 'From:')]"):
                    if bad.xpath(".//*[contains(text(), 'Genetics Home Reference')]"):
                        bad.getparent().remove(bad)

                gene["description"] = ""

                try:
                    gene_desc = "".join([tostring(el).decode("utf-8") for el in tree.xpath('./*')])
                    gene["description"] =  gene_desc
                except Exception as e:
                    print(str(e))
                    pass

                '''
                        PUT GENE in MONGODB
                '''

                print("parsed gene")
                queue.put(gene)
                break

            except Exception as e:
                print(str(e))
                #self.open_html(self.response.text)
                continue


    def open_html(self, html):
        path = os.path.abspath('temp.html')
        url =  path

        with open(path, 'w', encoding="utf-8") as f:
            f.write(html)

        webbrowser.open(url)


    def get_last_page(self, tree):
        return int(tree.xpath('//a[contains(@onclick, "ajaxPagingBondSearch")]//text()')[-1])

    def chunkIt(self, seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out

    def open_html(self, html):
        path = os.path.abspath('temp.html')
        url =  path

        with open(path, 'w', encoding="utf-8") as f:
            f.write(html)

        webbrowser.open(url)


def main():
    from pprint import pprint
    start_time = time.time()

    #-------------
    p = GenesParser()

    genes = p.parse()

    blah = []
    for gene in genes:
        blah.append(gene)

    with open('data.json', 'w', encoding="utf-8") as outfile:
        json.dump(blah, outfile)

    elapsed_time = time.time() - start_time
    print("time elapsed: ", elapsed_time)


if __name__ == '__main__':
    main()
