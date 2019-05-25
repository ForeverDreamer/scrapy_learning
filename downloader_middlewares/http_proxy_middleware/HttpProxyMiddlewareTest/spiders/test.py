# -*- coding: utf-8 -*-
import scrapy
import logging

logger = logging.getLogger("test spider")


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["http://crawleruniverse.com"]
    website_possible_httpstatus_list = [403]
    handle_httpstatus_list = [403]
    
    start_urls = (
        'http://crawleruniverse.com:8000/ct/ps',
    )

    def parse(self, response):
        res = response.body.decode('utf-8')
        if res == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            logger.info("got page: {}".format(res))
            yield response.request
