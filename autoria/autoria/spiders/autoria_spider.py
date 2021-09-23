import scrapy
from autoria.items import CarItem


class AutoriaSpider(scrapy.Spider):
    name = 'autoria'

    def start_requests(self):
        url = 'https://auto.ria.com/uk/legkovie/tesla/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        car_cards = response.css('div.content')
        for car_card in car_cards:
            car = CarItem()
            car['model'] = car_card.css('span::text').get().strip()
            car['year'] = car_card.css('div.head-ticket a[class="address"]::text')[1].get().strip()
            car['mileage'] = car_card.css('li[class="item-char js-race"]::text').get().strip()
            car['price_uah'] = car_card.css('span[data-currency="UAH"]::text').get()
            car['price_usd'] = car_card.css('span[data-currency="USD"]::text').get()
            car['vin_code'] = self.extract_vin_code(car_card.css('span.label-vin span'))
            car['link'] = car_card.css('a::attr(href)').get()
            yield car

        next_page_button = response.css('span[class="page-item next text-r"]')
        next_page_is_available = 'disabled' not in next_page_button.css('a::attr(class)').get()
        if next_page_is_available:
            url = next_page_button.css('a::attr(href)').get()
            yield scrapy.Request(url=url, callback=self.parse)

    def extract_vin_code(self, vin_code_parts):
        vin_code = ''
        for vin_part in vin_code_parts:
            span_text = vin_part.css('span::text').get().strip()
            if span_text.startswith(('AUTO.RIA', 'Перевірено')):
                break
            vin_code += span_text
        return vin_code


