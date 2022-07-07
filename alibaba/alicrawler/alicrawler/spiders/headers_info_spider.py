# 每个spider应该可以对应多个产品，每个产品对应一个Item，每个Item对应各自的django model

import scrapy


class HeadersInfoSpider(scrapy.Spider):
    name = 'headers_info_spider'

    start_urls = ['http://127.0.0.1:8000/ct/ri']

    def parse(self, response):
        pass