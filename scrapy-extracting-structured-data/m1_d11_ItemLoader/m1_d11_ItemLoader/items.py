# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import MapCompose

USDINR = 68


def convert_price(price):
    if price:
        return float(price.replace(',', '')) / USDINR


def shorten_amazon_link(link):
    product_id = link.split('/')[-1]
    return 'https://amazon.in/dp/' + product_id


class ProductItem(scrapy.Item):

    title = scrapy.Field()

    price = scrapy.Field(input_processor=MapCompose(convert_price))

    link = scrapy.Field(input_processor=MapCompose(shorten_amazon_link))
