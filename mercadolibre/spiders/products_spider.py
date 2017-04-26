import scrapy
class ProductsSpider(scrapy.Spider):
    name = "mercado2"
    start_urls = ['http://carros.mercadolibre.com.co/accesorios-para-carros/']

    def parse(self, response):
        for element in response.xpath('//li[contains(@class, "results-item list-view-item rowItem ")]'):
            yield {
                'title': element.xpath('//h2/a/text()').extract(),
            }

        next_page = response.xpath('//ul[contains(@class, "ch-pagination")]/li[contains(@class, "last-child")]/a/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
