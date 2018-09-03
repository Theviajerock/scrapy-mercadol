import scrapy
import re
from datetime import date
class ProductsSpider(scrapy.Spider):
    name = "mercadolibre2"
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'info ml.csv'
    }
    start_urls = ['https://computacion.mercadolibre.com.co/',
    'https://listado.mercadolibre.com.co/hogar-muebles/',
    'https://carros.mercadolibre.com.co/accesorios/',
    'https://motos.mercadolibre.com.co/accesorios/',
    'https://carros.mercadolibre.com.co/audio/',
    'https://vehiculos.mercadolibre.com.co/herramientas/',
    'https://carros.mercadolibre.com.co/repuestos/',
    'https://vehiculos.mercadolibre.com.co/tuning-performance/',
    'https://carros.mercadolibre.com.co/otros/',
    'https://listado.mercadolibre.com.co/electrodomesticos/',
    'https://listado.mercadolibre.com.co/camaras-accesorios/',
    'https://celulares.mercadolibre.com.co/accesorios/',
    'https://listado.mercadolibre.com.co/salud-belleza/',
    'https://deportes.mercadolibre.com.co/',
    'https://electronica.mercadolibre.com.co/',
    'https://videojuegos.mercadolibre.com.co/',
    'https://listado.mercadolibre.com.co/herramientas-construccion/',
    'https://listado.mercadolibre.com.co/animales-mascotas/',
    'https://listado.mercadolibre.com.co/industrias-y-oficinas/',
    'https://listado.mercadolibre.com.co/instrumentos-musicales/',
    'https://servicios.mercadolibre.com.co/',
    'https://listado.mercadolibre.com.co/otras-categorias/',
    'https://listado.mercadolibre.com.co/relojes-joyas/',
    'https://listado.mercadolibre.com.co/libros-revistas-comics/',
    'https://coleccionables.mercadolibre.com.co/',
    'https://listado.mercadolibre.com.co/alimentacion-bebes/',
    'https://listado.mercadolibre.com.co/higiene-cuidado-del-bebe/',
    'https://listado.mercadolibre.com.co/bebes/']
    # start_urls = ['']
    def parse(self, response):
        for element in response.xpath('//h2[contains(@class, "item__title list-view-item-title")]/a/@href').extract():
            yield scrapy.Request(element,callback=self.parse_product)

        #next_page = response.xpath('//li[contains(@class, "pagination__next")]/a/@href').extract_first()
        next_page = response.xpath('//li[contains(@class, "andes-pagination__button andes-pagination__button--next")]/a/@href').extract_first()
        print("new pagina")
        if next_page is not None:
            print("sig pagina")
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
                    formattedS_number = 0
                return formatted_number

        def check_text(html_element):
            if html_element is None:
                return ""
            else:
                return html_element.strip().translate(str.maketrans(dict.fromkeys(',')))
        # Get the info about the product, if is used or new
        condition1 = response.xpath('//div[contains(@class, "item-conditions")]/text()').extract_first()
        if "Usado" in condition1 or condition1 is None or check_numb(condition1) < 10:
            pass
        else:
            yield {
                'id' : response.xpath(".//input[starts-with(@name, 'item_id')]/@value").extract(),
            	'title': check_text(response.xpath('//h1[contains(@class, "item-title__primary ")]/text()').extract_first()),
            	'category' : check_text(response.xpath('//ul[contains(@class, "vip-navigation-breadcrumb-list")]/li[2]/a/text()').extract_first()),
    	        'price': check_numb(response.xpath('//span[contains(@class, "price-tag-fraction")]/text()').extract_first()),
            	'sold_products': check_numb(condition1),
            	'profit' : check_numb(response.xpath('//span[contains(@class, "price-tag-fraction")]/text()').extract_first())*check_numb(condition1),
                'url': response.url,
                'fecha_info' : date.today()
            }
