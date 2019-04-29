import scrapy

class EmailItem(scrapy.Item):
    url = scrapy.Field()
    email = scrapy.Field()
