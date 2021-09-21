import scrapy


class AutoriaSpider(scrapy.Spider):
    name = 'autoria'

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass