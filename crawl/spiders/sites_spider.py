import scrapy
import csv
import bs4
import re
import pandas as pd
import time
import sqlite3
from scrapy.utils.python import to_native_str
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)


class SitesSpider(scrapy.Spider):
    name = "heritage"
    urls = []
    # furls = []
    eresults = {}
    fresults = {}
    estatus = {}
    fstatus = {}
    dstatus = {}

    def start_requests(self):
        df = pd.read_excel(
            '/Users/scottsyms/code/HeritageCanada/data/Python Results.xlsx')
        count = 0
        for index, row in df.iterrows():
            count += 1
            # , "handle_httpstatus_all": True}
            site = {"language": "en", "pairid": count,
                    "url": row["EnglishURL"], "altURL": row["FrenchURL"], "OriginalURL": row["EnglishURL"], "playwright": True}
            yield scrapy.Request(url=site["url"], callback=self.parse, meta=site)
            # , "handle_httpstatus_all": True}
            site = {"language": "fr", "pairid": count,
                    "url": row["FrenchURL"], "altURL": row["EnglishURL"], "OriginalURL": row["FrenchURL"], "playwright": True}
            yield scrapy.Request(url=site["url"], callback=self.parse, meta=site)

    def parse(self, response):

        # If the response is a redirect, assemble the new URL and add a request to the iterator stack
        # if response.status in [301, 302]:
        #     newurl = response.urljoin(
        #         response.headers['Location'].decode("utf-8"))
        #     yield scrapy.Request(url=newurl, callback=self.parse, meta=response.meta)

        # if response.status == 200:
        # Remove the HTML from the response body
        text = bs4.BeautifulSoup(response.body, "lxml").text.strip()
        text = [line for line in text.split('\n') if line.strip() != '']

        # Remove lines with less than 5 words
        text = [line for line in text if len(line.split()) > 5]
        text = '\n'.join(text)

        # Yield selected reponse fields
        yield {'status': response.status, 'url': response.meta["OriginalURL"], 'language': response.meta["language"], 'text': text, "altURL": response.meta["altURL"], "pairid": response.meta["pairid"]}
