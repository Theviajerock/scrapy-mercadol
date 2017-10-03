import scrapy
import re
class ProductsSpider(scrapy.Spider):
    name = "mercado2"
    start_urls = ['https://deportes.mercadolibre.com.co/bicicletas-ciclismo/repuestos/']

    def parse(self, response):
#        def parse_details(self, response):
        for element in response.xpath('//h2[contains(@class, "item__title list-view-item-title")]/a/@href').extract():
            yield scrapy.Request(element,callback=self.parse_product)

        next_page = response.xpath('//li[contains(@class, "pagination__next")]/a/@href').extract_first()
        if next_page is not None:
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        item = response.meta.get('item', None)
        if item:
        # populate more `item` fields
           return item
        else:
            self.logger.warning('No item received for %s', response.url)
            print(response.status)

        def check_numb(html_element):
            """Function that receives a html element, check if
            this element is None, or if the element is for price
            and return the element formatted as an INT"""
            if html_element is None:
                return 0
            else:
                unformatted_number = html_element.strip()
                try:
                    formatted_number = int(re.sub('[^\d]', '', unformatted_number))
                except ValueError:
                    formatted_number = 0
                return formatted_number

        def check_text(html_element):
            if html_element is None:
                return ""
            else:
                return html_element.strip()
        # Get the info about the product, if is used or new
        condition1 = response.xpath('//div[contains(@class, "item-conditions")]/text()').extract_first()
        try:
            if "Usado" in condition1 or condition1 is None:
                return 0
        except ValueError:
            return 0

        yield {
            'title': check_text(response.xpath('//h1[contains(@class, "item-title__primary ")]/text()').extract_first()),
            'price': response.xpath('//span[contains(@class, "price-tag-fraction")]/text()').extract_first(),
            'condition1': check_numb(condition1),
            'url_images': response.xpath('//a[contains(@class, "gallery-trigger ch-zoom-trigger")]/img/@src').extract(),
            'category' : check_text(response.xpath('//ul[contains(@class, "vip-navigation-breadcrumb-list")]/li[2]/a/text()').extract_first())
            }


