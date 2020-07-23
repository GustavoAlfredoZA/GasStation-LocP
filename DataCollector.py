#!/usr/bin/env python3
import scrapy
from scrapy.item import Item
from scrapy.item import Field
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import urllib.request
import string
#import pandas as pd
import subprocess
import json

#pip install scrapy
#url https://datos.gob.mx/busca/dataset/estaciones-de-servicio-gasolineras-y-precios-finales-de-gasolina-y-diesel
#ElementTree https://docs.python.org/3/library/xml.etree.elementtree.html

p = open("routes.json")
routes = json.load(p)
ProyectPATH=routes['proyect']
PublicPATH=routes['public']
p.close()

class GasItem(Item):
    Name=Field()
    Link=Field()
    DateTime=Field()
    Type=Field()

class GasSpider(scrapy.Spider):
    name = "A"
    start_urls = ['https://datos.gob.mx/busca/dataset/estaciones-de-servicio-gasolineras-y-precios-finales-de-gasolina-y-diesel']
    def parse(self, response):
        i=0
        for sel in response.xpath('/html/body/div[2]/div[3]/div/div/div/div/div[2]/div[1]/div/div[3]/ul/div[1]/a'):
            item = GasItem()
            T = datetime.now()
            item['Name'] = T.strftime("%Y-%m-%dT%H_%M_%S-")+str(i)
            item['Link'] = sel.xpath('@href').extract()[0]
            item['DateTime'] = T
            item['Type']=i
            #record.loc[len(record)]=[item['Name'],item['Link'],item['DateTime'],item['Type']]
            urllib.request.urlretrieve(item['Link'],item['Name']+".xml")
            i+=1
            yield item
            filename=item['Name']+".xml"
            #output = subprocess.run(["scp",filename,"quantics@132.247.186.67:public_html/static"])
            #output = subprocess.run(["mv",filename,"backup/"])

#try:
#    record=pd.DataFrame(pd.read_csv("record.csv"))
#except Exception as e:
#    record=pd.DataFrame(columns=['Name','Link','DateTime','Type'])
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(GasSpider)
process.start()
#print(record)
#record.to_csv("record.csv",index=False)
