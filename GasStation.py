import scrapy
from scrapy.item import Item
from scrapy.item import Field
from scrapy.crawler import CrawlerProcess
import datetime
from datetime import datetime
import urllib
import urllib.request
import string

#pip install scrapy
#url https://datos.gob.mx/busca/dataset/estaciones-de-servicio-gasolineras-y-precios-finales-de-gasolina-y-diesel
#wget=https://bit.ly/2V1Z3sm
#wget=https://bit.ly/2JNcTha

class GasItem(Item):
    Name=Field()
    Link=Field()
    DateTime=Field()

class GasSpider(scrapy.Spider):
    name = "A"
    start_urls = ['https://datos.gob.mx/busca/dataset/estaciones-de-servicio-gasolineras-y-precios-finales-de-gasolina-y-diesel']
    def parse(self, response):
        i=0
        for sel in response.xpath('/html/body/div[2]/div[3]/div/div/div/div/div[2]/div[1]/div/div[3]/ul/div[1]/a'):
            item = GasItem()
            T = datetime.now()
            item['Name'] = str(i)+T.strftime("D%Y-%m-%dT%H_%M_%S")
            item['Link'] = sel.xpath('@href').extract()
            item['DateTime'] = T
            urllib.request.urlretrieve(item['Link'][0],item['Name']+".csv")
            i+=1
            yield item

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(GasSpider)
process.start()
