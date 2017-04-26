import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

class MercadoSpider(scrapy.Spider):
    name = 'mercado'
    #item_count = 0
    #allowed_domain = ['www.mercadolibre.com.mx']
    start_urls = ['http://computacion.mercadolibre.com.mx/impresoras/impresoras/']

    rules = {
        # Para cada item
        Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="last-child"]/a'))),
        Rule(LinkExtractor(allow =(), restrict_xpaths = ('//h2[@class="list-view-item-title"]')),
                            callback = 'parse', follow = False)
    }

    def parse(self, response):
        #info de producto
        yield {
            'titulo': response.xpath('normalize-space(/html/body/main/div/section[2]/header/h1/text())').extract_first(),
            'folio' : response.xpath('normalize-space(//span[@class="id-item"]/text())').extract()
        }
        """
        self.item_count += 1
        if self.item_count > 10:
            raise CloseSpider('item_exceeded')
        yield ml_item
        """
