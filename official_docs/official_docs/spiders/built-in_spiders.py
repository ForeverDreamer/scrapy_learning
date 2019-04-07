# -*- coding: utf-8 -*-

# import scrapy
# from official_docs.items import MyItem
#
#
#
# class MySpider(scrapy.Spider):
#     name = 'myspider'
#
#     # example 1
#     # def start_requests(self):
#     #     return [scrapy.FormRequest("http://www.example.com/login",
#     #                                formdata={'user': 'john', 'pass': 'secret'},
#     #                                callback=self.logged_in)]
#     #
#     # def logged_in(self, response):
#     #     # here you would extract links to follow and return Requests for
#     #     # each of them, with another callback
#     #     self.logger.info(response.text)
#
#
#     # example 2
#     # allowed_domains = ['example.com']
#     # start_urls = [
#     #     'http://www.example.com/1.html',
#     #     'http://www.example.com/2.html',
#     #     'http://www.example.com/3.html',
#     # ]
#     #
#     # def parse(self, response):
#     #     self.logger.info('A response from %s just arrived!', response.url)
#
#
#     # example 3
#     # allowed_domains = ['example.com']
#     # start_urls = [
#     #     'http://www.example.com/1.html',
#     #     'http://www.example.com/2.html',
#     #     'http://www.example.com/3.html',
#     # ]
#     #
#     # def parse(self, response):
#     #     for h3 in response.xpath('//h3').getall():
#     #         yield {"title": h3}
#     #
#     #     for href in response.xpath('//a/@href').getall():
#     #         yield scrapy.Request(response.urljoin(href), self.parse)
#
#
#     # example 4
#     # allowed_domains = ['example.com']
#     #
#     # def start_requests(self):
#     #     yield scrapy.Request('http://www.example.com/1.html', self.parse)
#     #     yield scrapy.Request('http://www.example.com/2.html', self.parse)
#     #     yield scrapy.Request('http://www.example.com/3.html', self.parse)
#     #
#     # def parse(self, response):
#     #     for h3 in response.xpath('//h3').getall():
#     #         yield MyItem(title=h3)
#     #
#     #     for href in response.xpath('//a/@href').getall():
#     #         yield scrapy.Request(response.urljoin(href), self.parse)
#
#
#     # example 5
#     # def __init__(self, category=None, *args, **kwargs):
#     #     super(MySpider, self).__init__(*args, **kwargs)
#     #     self.start_urls = ['http://www.example.com/categories/%s' % category]
#
#
#     # example 6
#     def start_requests(self):
#         yield scrapy.Request('http://www.example.com/categories/%s' % self.category)


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from official_docs.items import TestItem


class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        # item = scrapy.Item()
        item = TestItem()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').get()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').get()
        return item
