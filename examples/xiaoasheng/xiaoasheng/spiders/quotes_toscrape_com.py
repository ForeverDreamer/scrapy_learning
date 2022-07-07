import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

from ..items import SynopsisItem, AuthorItem


class IntroSpider(scrapy.Spider):
    name = "quotes_toscrape_com"

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response, **kwargs):

        # Extract the list of book titles into a list
        quotes = response.css('div.quote')

        for quote in quotes:
            product_loader = ItemLoader(item=SynopsisItem(), selector=quote)
            product_loader.default_output_processor = TakeFirst()

            product_loader.add_css('text', '.text::text')
            product_loader.add_css('author', '.author::text')
            product_loader.add_css('tags', '.tag::text')

            yield product_loader.load_item()

            author_url = quote.css('.author + a::attr(href)').get()
            self.logger.info('get author page url')
            # go to the author page
            yield response.follow(author_url, callback=self.parse_author)

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

    def parse_author(self, response):
        self.logger.info('parsing author...')
        product_loader = ItemLoader(item=AuthorItem(), selector=response)
        product_loader.default_output_processor = TakeFirst()

        product_loader.add_css('name', '.author-title::text')
        product_loader.add_css('birthday', '.author-born-date::text')
        product_loader.add_css('bornlocation', '.author-born-location::text')
        product_loader.add_css('description', '.author-description::text')

        yield product_loader.load_item()
