import scrapy
from scrapy.loader.processors import MapCompose


def process_url(value):
    domain = 'https://stackoverflow.com'
    comp_url = domain + value
    return comp_url


class QuestionItem(scrapy.Item):

    question = scrapy.Field()

    url = scrapy.Field(input_processor=MapCompose(process_url))
