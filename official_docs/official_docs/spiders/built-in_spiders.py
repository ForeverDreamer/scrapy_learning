# scrapy.Spider examples

import scrapy
# from official_docs.items import MyItem


class MySpider(scrapy.Spider):
    name = 'myspider'

    # example 1
    # def start_requests(self):
    #     return [scrapy.FormRequest("http://www.example.com/login",
    #                                formdata={'user': 'john', 'pass': 'secret'},
    #                                callback=self.logged_in)]
    #
    # def logged_in(self, response):
    #     # here you would extract links to follow and return Requests for
    #     # each of them, with another callback
    #     self.logger.info(response.text)


    # example 2
    # allowed_domains = ['example.com']
    # start_urls = [
    #     'http://www.example.com/1.html',
    #     'http://www.example.com/2.html',
    #     'http://www.example.com/3.html',
    # ]
    #
    # def parse(self, response):
    #     self.logger.info('A response from %s just arrived!', response.url)


    # example 3
    # allowed_domains = ['example.com']
    # start_urls = [
    #     'http://www.example.com/1.html',
    #     'http://www.example.com/2.html',
    #     'http://www.example.com/3.html',
    # ]
    #
    # def parse(self, response):
    #     for h3 in response.xpath('//h3').getall():
    #         yield {"title": h3}
    #
    #     for href in response.xpath('//a/@href').getall():
    #         yield scrapy.Request(response.urljoin(href), self.parse)


    # example 4
    # allowed_domains = ['example.com']
    #
    # def start_requests(self):
    #     yield scrapy.Request('http://www.example.com/1.html', self.parse)
    #     yield scrapy.Request('http://www.example.com/2.html', self.parse)
    #     yield scrapy.Request('http://www.example.com/3.html', self.parse)
    #
    # def parse(self, response):
    #     for h3 in response.xpath('//h3').getall():
    #         yield MyItem(title=h3)
    #
    #     for href in response.xpath('//a/@href').getall():
    #         yield scrapy.Request(response.urljoin(href), self.parse)


    # example 5
    # def __init__(self, category=None, *args, **kwargs):
    #     super(MySpider, self).__init__(*args, **kwargs)
    #     self.start_urls = ['http://www.example.com/categories/%s' % category]


    # example 6
    # def start_requests(self):
    #     yield scrapy.Request('http://www.example.com/categories/%s' % self.category)


# Generic Spiders examples

# CrawlSpider example
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from official_docs.items import TestItem
#
#
# class MySpider(CrawlSpider):
#     name = 'example.com'
#     allowed_domains = ['example.com']
#     start_urls = ['http://www.example.com']
#
#     rules = (
#         # Extract links matching 'category.php' (but not matching 'subsection.php')
#         # and follow links from them (since no callback means follow=True by default).
#         Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
#
#         # Extract links matching 'item.php' and parse them with the spider's method parse_item
#         Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
#     )
#
#     def parse_item(self, response):
#         self.logger.info('Hi, this is an item page! %s', response.url)
#         # item = scrapy.Item()
#         item = TestItem()
#         item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
#         item['name'] = response.xpath('//td[@id="item_name"]/text()').get()
#         item['description'] = response.xpath('//td[@id="item_description"]/text()').get()
#         return item


# XMLFeedSpider example
# from scrapy.spiders import XMLFeedSpider
# from official_docs.items import TestItem
#
#
# class MySpider(XMLFeedSpider):
#     name = 'example.com'
#     allowed_domains = ['example.com']
#     start_urls = ['http://www.example.com/feed.xml']
#     iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
#     itertag = 'item'
#
#     def parse_node(self, response, node):
#         self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.getall()))
#
#         item = TestItem()
#         item['id'] = node.xpath('@id').get()
#         item['name'] = node.xpath('name').get()
#         item['description'] = node.xpath('description').get()
#         return item


# CSVFeedSpider example
# from scrapy.spiders import CSVFeedSpider
# from official_docs.items import TestItem
#
#
# class MySpider(CSVFeedSpider):
#     name = 'example.com'
#     allowed_domains = ['example.com']
#     start_urls = ['http://www.example.com/feed.csv']
#     delimiter = ';'
#     quotechar = "'"
#     headers = ['id', 'name', 'description']
#
#     def parse_row(self, response, row):
#         self.logger.info('Hi, this is a row!: %r', row)
#
#         item = TestItem()
#         item['id'] = row['id']
#         item['name'] = row['name']
#         item['description'] = row['description']
#         return item


# SitemapSpider examples

# from datetime import datetime
# from scrapy.spiders import SitemapSpider
#
#
# class FilteredSitemapSpider(SitemapSpider):
#     name = 'filtered_sitemap_spider'
#     allowed_domains = ['example.com']
#     sitemap_urls = ['http://example.com/sitemap.xml']
#
#     def sitemap_filter(self, entries):
#         for entry in entries:
#             date_time = datetime.strptime(entry['lastmod'], '%Y-%m-%d')
#             if date_time.year >= 2005:
#                 yield entry


# Simplest example: process all urls discovered through sitemaps using the parse callback:
# from scrapy.spiders import SitemapSpider
#
#
# class MySpider(SitemapSpider):
#     sitemap_urls = ['http://www.example.com/sitemap.xml']
#
#     def parse(self, response):
#         pass # ... scrape item here ...


# Process some urls with certain callback and other urls with a different callback:
# from scrapy.spiders import SitemapSpider
#
#
# class MySpider(SitemapSpider):
#     sitemap_urls = ['http://www.example.com/sitemap.xml']
#     sitemap_rules = [
#         ('/product/', 'parse_product'),
#         ('/category/', 'parse_category'),
#     ]
#
#     def parse_product(self, response):
#         pass # ... scrape product ...
#
#     def parse_category(self, response):
#         pass # ... scrape category ...


# Follow sitemaps defined in the robots.txt file and only follow sitemaps whose url contains /sitemap_shop:
# from scrapy.spiders import SitemapSpider
#
#
# class MySpider(SitemapSpider):
#     sitemap_urls = ['http://www.example.com/robots.txt']
#     sitemap_rules = [
#         ('/shop/', 'parse_shop'),
#     ]
#     sitemap_follow = ['/sitemap_shops']
#
#     def parse_shop(self, response):
#         pass # ... scrape shop here ...


# Combine SitemapSpider with other sources of urls:
# import scrapy
# from scrapy.spiders import SitemapSpider
# 
# 
# class MySpider(SitemapSpider):
#     name = 'myspider'
#     sitemap_urls = ['http://www.example.com/robots.txt']
#     sitemap_rules = [
#         ('/shop/', 'parse_shop'),
#     ]
# 
#     other_urls = ['http://www.example.com/about']
# 
#     def start_requests(self):
#         requests = list(super(MySpider, self).start_requests())
#         requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
#         return requests
# 
#     def parse_shop(self, response):
#         pass # ... scrape shop here ...
# 
#     def parse_other(self, response):
#         pass # ... scrape other here ...