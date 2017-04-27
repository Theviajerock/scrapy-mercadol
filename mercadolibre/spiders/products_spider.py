import scrapy
import re
class ProductsSpider(scrapy.Spider):
    name = "mercado2"
    start_urls = ['http://carros.mercadolibre.com.co/accesorios-para-carros/']

    def parse(self, response):
        for element in response.xpath('//li[contains(@class, "results-item list-view-item rowItem ")]/h2/a/@href').extract():
            yield scrapy.Request(element,callback=self.parse_product)

        next_page = response.xpath('//ul[contains(@class, "ch-pagination")]/li[contains(@class, "last-child")]/a/@href').extract_first()
        if next_page is not None:
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        def check_numb(html_element):
            """Function that receives a html element, check if
            this element is None, or if the element is for price
            and return the element formatted as an INT"""
            if html_element is None:
                return 0
            else:
                unformatted_number = html_element.strip()
                formatted_number = int(re.sub('[^\d]', '', unformatted_number))
                return formatted_number

        def check_text(html_element):
            if html_element is None:
                return ""
            else:
                return html_element.strip()

        yield {
            'title': check_text(response.xpath('//h1[contains(@class, "vip-title-main ")]/text()').extract_first()),
            'price': check_numb(response.xpath('//article[contains(@class, "vip-price ch-price")]/strong/text()').extract_first()),
            'condition1': check_text(response.xpath('//div[contains(@class, "item-conditions")]/dd[1]/text()').extract_first()),
            'condition2': check_numb(response.xpath('//div[contains(@class, "item-conditions")]/dd[2]/text()').extract_first()),
            'url_images': response.xpath('//*[contains(@class, "gallery-trigger")]/img/@src').extract()
            }


