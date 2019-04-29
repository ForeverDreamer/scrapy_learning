import re
import csv

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import replace_escape_chars
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from m2_d03_BroadCrawler.items import EmailItem

# CrawlSpider is the most commonly used spider for crawling regular websites, 
# as it provides a convenient mechanism for following links by defining a set of rules

# Scrapy uses 'twisted' which is asynchronous. If you set concurrent_requests as 10 then, it will 
# make 10 requests asynchronous at a time when out of those ten request any of the requests are complete then 
# another one is added up in the queue.
# Note: the CPU usage shoots up to 90ish when you set concurrent requests to 80
# At 2 concurrent request doesn't go beyond 60something.
# at 20 concurrent requests shows the same behaviour as the 80 requests. 


# First start with only 'loonycorn.in' domain in the list 
# next start with 'redirect'= off  in settings.py and enable only 'Paytm.in' - to show the redirect 
# Then enable redirect ON and enable all the domains except 'loonycorn'
# changes are to be made in settings.py
# Case 1: Only way to show is that time  - i.e. set the no of requests to 2 or 1 compare the 
# Case 2: start time and finish time. Then, set it to 20; compare the start and finish time. 
# Show the CPU usage for the both cases


class BroadCrawl(CrawlSpider):

    name = 'scrape_emails'

    start_urls = ['http://www.columbia.edu/',
                  'https://www.espn.com',
                  'https://www.loonycorn.in',
                  'https://www.paytm.in'
                  ]

    rules = (Rule(LinkExtractor(), callback='parse_item'),)

    def parse_item(self, response):
       
        loader_object = ItemLoader(item=EmailItem(), response=response)

        loader_object.default_output_processor = MapCompose(lambda x: x.strip(), replace_escape_chars)

        emails = response.xpath('//text()').re(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}")

        if emails:
            loader_object.add_value('email', emails)
            loader_object.add_value('url', response.url)

        # with open('email_list.txt','a+') as f:
        #     if len(emails) != 0:
        #         f.write(str(emails) + "   " + response.url + "\n")

        return loader_object.load_item()
