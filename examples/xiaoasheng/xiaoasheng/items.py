# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Identity, Join, MapCompose


def process_text(text):
    return text.strip()


def process_author(author):
    return author.strip()


def process_tags(tags):
    return tags


class SynopsisItem(scrapy.Item):
    text = scrapy.Field(input_processor=MapCompose(process_text))
    author = scrapy.Field(input_processor=MapCompose(process_author))
    tags = scrapy.Field(input_processor=MapCompose(process_tags), output_processor=Identity())


def process_author_name(name):
    return name.strip()


def process_author_birthday(birthday):
    return birthday.strip()


def process_author_bornlocation(bornlocation):
    return bornlocation.strip()


def process_author_description(description):
    return description.strip()


class AuthorItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(process_author_name))
    birthday = scrapy.Field(input_processor=MapCompose(process_author_birthday))
    bornlocation = scrapy.Field(input_processor=MapCompose(process_author_bornlocation))
    description = scrapy.Field(input_processor=MapCompose(process_author_description))
